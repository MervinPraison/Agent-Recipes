"""
Main pipeline orchestrator for AI Video Editor.

Provides the high-level edit(), probe(), and transcript() functions.
"""

import os
from pathlib import Path
from typing import Optional

from .config import PRESETS
from .models import TranscriptResult, VideoEditResult, VideoProbeResult
from .ffmpeg_probe import probe as probe_video
from .transcribe import transcript as transcribe_video
from .llm_plan import analyze_content, create_simple_edit_plan
from .timeline import optimize_timeline, calculate_final_duration
from .render import render as render_video
from .utils import (
    check_ffmpeg,
    create_workdir,
    file_hash,
    format_duration,
    generate_edl,
    parse_duration,
    save_config_snapshot,
)


def probe(input_path: str) -> VideoProbeResult:
    """
    Probe a video file to extract metadata.
    
    Args:
        input_path: Path to video file
        
    Returns:
        VideoProbeResult with video metadata
    """
    return probe_video(input_path)


def transcript(
    input_path: str,
    provider: str = "auto",
    language: str = "en",
    workdir: str = None
) -> TranscriptResult:
    """
    Transcribe audio/video with word-level timestamps.
    
    Args:
        input_path: Path to audio or video file
        provider: Transcription provider (openai, local, auto)
        language: Language code
        workdir: Working directory for temp files
        
    Returns:
        TranscriptResult with text and word timestamps
    """
    return transcribe_video(input_path, provider=provider, language=language, workdir=workdir)


def edit(
    input_path: str,
    output_path: Optional[str] = None,
    preset: str = "podcast",
    workdir: Optional[str] = None,
    remove_fillers: Optional[bool] = None,
    remove_repetitions: Optional[bool] = None,
    remove_tangents: Optional[bool] = None,
    remove_silence: Optional[bool] = None,
    auto_crop: str = "off",
    target_length: Optional[str] = None,
    captions: str = "srt",
    provider: str = "auto",
    use_llm: bool = True,
    force: bool = False,
    verbose: bool = False
) -> VideoEditResult:
    """
    Edit a video using AI-powered analysis.
    
    Args:
        input_path: Path to input video file
        output_path: Path for output video (default: input_edited.mp4)
        preset: Edit preset (podcast, meeting, course, clean)
        workdir: Working directory for temp files
        remove_fillers: Remove filler words (overrides preset)
        remove_repetitions: Remove repeated phrases (overrides preset)
        remove_tangents: Remove off-topic content (overrides preset)
        remove_silence: Remove long silences (overrides preset)
        auto_crop: Cropping mode (off, center, face)
        target_length: Target output duration (e.g., "6m", "90s")
        captions: Caption mode (off, srt, burn)
        provider: Transcription provider (openai, local, auto)
        use_llm: Use LLM for content analysis (False = simple pattern matching)
        force: Overwrite output if exists
        verbose: Print progress messages
        
    Returns:
        VideoEditResult with paths to output files and metadata
    """
    def _log(message: str):
        if verbose:
            print(f"[AI Video Editor] {message}")
    
    # Validate input
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")
    
    # Check ffmpeg
    available, msg = check_ffmpeg()
    if not available:
        raise RuntimeError(f"FFmpeg is required: {msg}")
    
    _log(f"Starting edit of: {input_path}")
    
    # Set up paths
    input_path = str(Path(input_path).absolute())
    
    if output_path is None:
        input_stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{input_stem}_edited.mp4")
    
    output_path = str(Path(output_path).absolute())
    
    # Create working directory
    if workdir is None:
        work_path = create_workdir(input_path)
    else:
        work_path = Path(workdir)
        work_path.mkdir(parents=True, exist_ok=True)
    
    _log(f"Working directory: {work_path}")
    
    # Build configuration from preset + overrides
    config = _build_config(
        preset=preset,
        remove_fillers=remove_fillers,
        remove_repetitions=remove_repetitions,
        remove_tangents=remove_tangents,
        remove_silence=remove_silence,
        target_length=target_length
    )
    
    # Save config snapshot
    config_snapshot = {
        "input_path": input_path,
        "input_hash": file_hash(input_path),
        "preset": preset,
        "config": config,
        "auto_crop": auto_crop,
        "captions": captions,
        "provider": provider,
        "use_llm": use_llm
    }
    save_config_snapshot(config_snapshot, work_path)
    
    # Step 1: Probe video
    _log("Probing video...")
    video_probe = probe_video(input_path)
    _log(f"Duration: {format_duration(video_probe.duration)}, "
          f"Resolution: {video_probe.width}x{video_probe.height}")
    
    # Step 2: Transcribe
    _log("Transcribing audio...")
    transcript_result = transcribe_video(
        input_path,
        provider=provider,
        workdir=str(work_path)
    )
    _log(f"Transcribed {len(transcript_result.words)} words")
    
    # Save transcript
    transcript_path = work_path / "output" / "transcript.txt"
    transcript_path.parent.mkdir(exist_ok=True)
    transcript_path.write_text(transcript_result.text)
    
    srt_path = work_path / "output" / "captions.srt"
    transcript_result.to_srt(srt_path)
    
    # Step 3: Analyze content and create edit plan
    _log("Analyzing content...")
    if use_llm:
        edit_plan = analyze_content(transcript_result, config)
    else:
        edit_plan = create_simple_edit_plan(transcript_result, config)
    
    _log(f"Found {len(edit_plan.segments_to_remove)} segments to remove")
    
    # Step 4: Optimize timeline
    _log("Optimizing timeline...")
    edit_plan = optimize_timeline(edit_plan, transcript_result, config)
    
    # Step 5: Render
    _log("Rendering video...")
    render_video(
        input_path=input_path,
        output_path=output_path,
        edit_plan=edit_plan,
        probe=video_probe,
        workdir=work_path,
        crop_mode=auto_crop,
        normalize_audio=True,
        burn_captions=(captions == "burn"),
        srt_path=str(srt_path) if captions == "burn" else None,
        force=force
    )
    
    # Step 6: Generate reports
    _log("Generating reports...")
    
    # EDL file
    edl_path = work_path / "output" / "edit_decision_list.edl"
    generate_edl(
        segments_to_keep=[(s.start, s.end) for s in edit_plan.segments_to_keep],
        segments_to_remove=[(s.start, s.end, s.reason) for s in edit_plan.segments_to_remove],
        output_path=str(edl_path),
        fps=video_probe.fps
    )
    
    # Edit plan JSON
    plan_path = work_path / "output" / "edit_plan.json"
    edit_plan.to_json(plan_path)
    
    # Calculate final duration
    final_duration = calculate_final_duration(edit_plan)
    time_saved = video_probe.duration - final_duration
    
    # Build result
    result = VideoEditResult(
        output_path=output_path,
        report_path=str(plan_path),
        transcript_path=str(transcript_path),
        srt_path=str(srt_path),
        edl_path=str(edl_path),
        original_duration=video_probe.duration,
        final_duration=final_duration,
        time_saved=time_saved,
        edit_plan=edit_plan,
        probe=video_probe,
        transcript=transcript_result,
        workdir=str(work_path),
        config_snapshot=config_snapshot
    )
    
    # Save full report
    report_path = work_path / "output" / "report.json"
    result.to_json(report_path)
    
    _log("Edit complete!")
    _log(f"Original: {format_duration(video_probe.duration)}")
    _log(f"Final: {format_duration(final_duration)}")
    _log(f"Saved: {format_duration(time_saved)} ({(time_saved/video_probe.duration)*100:.1f}%)")
    _log(f"Output: {output_path}")
    
    return result


def _build_config(
    preset: str,
    remove_fillers: Optional[bool],
    remove_repetitions: Optional[bool],
    remove_tangents: Optional[bool],
    remove_silence: Optional[bool],
    target_length: Optional[str]
) -> dict:
    """Build configuration from preset and overrides."""
    
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset: {preset}. Available: {list(PRESETS.keys())}")
    
    config = PRESETS[preset].copy()
    
    if remove_fillers is not None:
        config["remove_fillers"] = remove_fillers
    if remove_repetitions is not None:
        config["remove_repetitions"] = remove_repetitions
    if remove_tangents is not None:
        config["remove_tangents"] = remove_tangents
    if remove_silence is not None:
        config["remove_silence"] = remove_silence
    
    if target_length:
        config["target_length"] = parse_duration(target_length)
    
    return config
