"""
Video rendering using FFmpeg.

Handles:
- Segment concatenation
- Cropping and scaling
- Audio normalization
- Caption burning
"""

import os
import subprocess
from pathlib import Path
from typing import List, Literal, Tuple

from .models import EditPlan, VideoProbeResult
from .timeline import get_keep_intervals
from .utils import ensure_ffmpeg


def render(
    input_path: str,
    output_path: str,
    edit_plan: EditPlan,
    probe: VideoProbeResult,
    workdir: Path,
    crop_mode: Literal["off", "center", "face"] = "off",
    normalize_audio: bool = False,
    burn_captions: bool = False,
    srt_path: str = None,
    force: bool = False
) -> str:
    """
    Render edited video.
    
    Args:
        input_path: Path to input video
        output_path: Path for output video
        edit_plan: Edit plan with segments to keep
        probe: Video probe result
        workdir: Working directory
        crop_mode: Cropping mode (off, center, face)
        normalize_audio: Normalize audio loudness
        burn_captions: Burn captions into video
        srt_path: Path to SRT file for captions
        force: Overwrite output if exists
        
    Returns:
        Path to rendered video
    """
    ensure_ffmpeg()
    
    if os.path.exists(output_path) and not force:
        raise FileExistsError(
            f"Output file already exists: {output_path}. "
            "Use force=True to overwrite."
        )
    
    intervals = get_keep_intervals(edit_plan)
    
    if not intervals:
        raise ValueError("No segments to keep in edit plan")
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if len(intervals) <= 10:
        return _render_filter_complex(
            input_path, output_path, intervals, probe,
            crop_mode, normalize_audio, burn_captions, srt_path
        )
    else:
        return _render_concat_demuxer(
            input_path, output_path, intervals, probe, workdir,
            crop_mode, normalize_audio, burn_captions, srt_path
        )


def _render_filter_complex(
    input_path: str,
    output_path: str,
    intervals: List[Tuple[float, float]],
    probe: VideoProbeResult,
    crop_mode: str,
    normalize_audio: bool,
    burn_captions: bool,
    srt_path: str
) -> str:
    """Render using filter_complex (efficient for few segments)."""
    
    filter_parts = []
    n = len(intervals)
    
    for i, (start, end) in enumerate(intervals):
        duration = end - start
        filter_parts.append(
            f"[0:v]trim=start={start}:duration={duration},setpts=PTS-STARTPTS[v{i}]"
        )
        filter_parts.append(
            f"[0:a]atrim=start={start}:duration={duration},asetpts=PTS-STARTPTS[a{i}]"
        )
    
    video_inputs = "".join(f"[v{i}]" for i in range(n))
    filter_parts.append(f"{video_inputs}concat=n={n}:v=1:a=0[vconcat]")
    
    audio_inputs = "".join(f"[a{i}]" for i in range(n))
    filter_parts.append(f"{audio_inputs}concat=n={n}:v=0:a=1[aconcat]")
    
    video_out = "[vconcat]"
    if crop_mode == "center":
        target_ratio = 9 / 16
        current_ratio = probe.width / probe.height
        
        if current_ratio > target_ratio:
            new_width = int(probe.height * target_ratio)
            crop_x = (probe.width - new_width) // 2
            filter_parts.append(f"[vconcat]crop={new_width}:{probe.height}:{crop_x}:0[vcrop]")
            video_out = "[vcrop]"
    
    audio_out = "[aconcat]"
    if normalize_audio:
        filter_parts.append("[aconcat]loudnorm=I=-16:TP=-1.5:LRA=11[anorm]")
        audio_out = "[anorm]"
    
    filter_complex = ";".join(filter_parts)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
    ]
    
    if burn_captions and srt_path and os.path.exists(srt_path):
        filter_complex += f";{video_out}subtitles='{srt_path}'[vfinal]"
        video_out = "[vfinal]"
    
    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", video_out,
        "-map", audio_out,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg render failed: {result.stderr}")
    
    return output_path


def _render_concat_demuxer(
    input_path: str,
    output_path: str,
    intervals: List[Tuple[float, float]],
    probe: VideoProbeResult,
    workdir: Path,
    crop_mode: str,
    normalize_audio: bool,
    burn_captions: bool,
    srt_path: str
) -> str:
    """Render using concat demuxer (efficient for many segments)."""
    
    segments_dir = workdir / "segments"
    segments_dir.mkdir(exist_ok=True)
    
    segment_files = []
    
    for i, (start, end) in enumerate(intervals):
        seg_path = segments_dir / f"seg_{i:04d}.mp4"
        duration = end - start
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", input_path,
            "-t", str(duration),
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            str(seg_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to extract segment {i}: {result.stderr}")
        
        segment_files.append(seg_path)
    
    concat_file = workdir / "concat.txt"
    with open(concat_file, "w") as f:
        for seg_path in segment_files:
            f.write(f"file '{seg_path}'\n")
    
    temp_output = workdir / "temp_concat.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(temp_output)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to concatenate segments: {result.stderr}")
    
    if crop_mode != "off" or normalize_audio or burn_captions:
        return _apply_post_processing(
            str(temp_output), output_path, probe,
            crop_mode, normalize_audio, burn_captions, srt_path
        )
    else:
        import shutil
        shutil.move(str(temp_output), output_path)
        return output_path


def _apply_post_processing(
    input_path: str,
    output_path: str,
    probe: VideoProbeResult,
    crop_mode: str,
    normalize_audio: bool,
    burn_captions: bool,
    srt_path: str
) -> str:
    """Apply post-processing filters."""
    
    filters_v = []
    filters_a = []
    
    if crop_mode == "center":
        target_ratio = 9 / 16
        current_ratio = probe.width / probe.height
        
        if current_ratio > target_ratio:
            new_width = int(probe.height * target_ratio)
            crop_x = (probe.width - new_width) // 2
            filters_v.append(f"crop={new_width}:{probe.height}:{crop_x}:0")
    
    if burn_captions and srt_path and os.path.exists(srt_path):
        filters_v.append(f"subtitles='{srt_path}'")
    
    if normalize_audio:
        filters_a.append("loudnorm=I=-16:TP=-1.5:LRA=11")
    
    cmd = ["ffmpeg", "-y", "-i", input_path]
    
    if filters_v:
        cmd.extend(["-vf", ",".join(filters_v)])
    
    if filters_a:
        cmd.extend(["-af", ",".join(filters_a)])
    
    cmd.extend([
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Post-processing failed: {result.stderr}")
    
    return output_path
