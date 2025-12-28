"""
CLI for AI Video Editor.

Provides command-line interface for:
- edit: Edit video with AI analysis
- probe: Extract video metadata
- transcript: Generate transcript with timestamps
- doctor: Check dependencies
"""

import argparse
import json
import os
import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="ai_video_editor",
        description="AI-powered video editor - removes fillers, repetitions, tangents, and silences"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit video with AI analysis")
    edit_parser.add_argument("input", help="Input video file")
    edit_parser.add_argument("-o", "--output", help="Output video file")
    edit_parser.add_argument("-p", "--preset", default="podcast",
                            choices=["podcast", "meeting", "course", "clean"],
                            help="Edit preset (default: podcast)")
    edit_parser.add_argument("--remove-fillers", action="store_true",
                            help="Remove filler words")
    edit_parser.add_argument("--remove-repetitions", action="store_true",
                            help="Remove repeated phrases")
    edit_parser.add_argument("--remove-tangents", action="store_true",
                            help="Remove off-topic content")
    edit_parser.add_argument("--remove-silence", action="store_true",
                            help="Remove long silences")
    edit_parser.add_argument("--auto-crop", default="off",
                            choices=["off", "center", "face"],
                            help="Cropping mode (default: off)")
    edit_parser.add_argument("--target-length", help="Target duration (e.g., 6m, 90s)")
    edit_parser.add_argument("--captions", default="srt",
                            choices=["off", "srt", "burn"],
                            help="Caption mode (default: srt)")
    edit_parser.add_argument("--provider", default="auto",
                            choices=["openai", "local", "auto"],
                            help="Transcription provider (default: auto)")
    edit_parser.add_argument("--no-llm", action="store_true",
                            help="Use simple pattern matching instead of LLM")
    edit_parser.add_argument("--force", action="store_true",
                            help="Overwrite output if exists")
    edit_parser.add_argument("--json-report", help="Save JSON report to path")
    edit_parser.add_argument("-v", "--verbose", action="store_true",
                            help="Enable verbose output")
    
    # Probe command
    probe_parser = subparsers.add_parser("probe", help="Extract video metadata")
    probe_parser.add_argument("input", help="Input video file")
    probe_parser.add_argument("--json", action="store_true",
                             help="Output as JSON")
    
    # Transcript command
    transcript_parser = subparsers.add_parser("transcript", help="Generate transcript")
    transcript_parser.add_argument("input", help="Input video/audio file")
    transcript_parser.add_argument("-o", "--output", help="Output file path")
    transcript_parser.add_argument("--format", default="srt",
                                  choices=["srt", "txt", "json"],
                                  help="Output format (default: srt)")
    transcript_parser.add_argument("--provider", default="auto",
                                  choices=["openai", "local", "auto"],
                                  help="Transcription provider (default: auto)")
    transcript_parser.add_argument("--language", default="en",
                                  help="Language code (default: en)")
    
    # Doctor command
    doctor_parser = subparsers.add_parser("doctor", help="Check dependencies")
    
    # Help command
    help_parser = subparsers.add_parser("help", help="Show help")
    
    args = parser.parse_args()
    
    if args.command is None or args.command == "help":
        _print_help()
        return 0
    
    try:
        if args.command == "edit":
            return cmd_edit(args)
        elif args.command == "probe":
            return cmd_probe(args)
        elif args.command == "transcript":
            return cmd_transcript(args)
        elif args.command == "doctor":
            return cmd_doctor(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if os.environ.get("DEBUG"):
            import traceback
            traceback.print_exc()
        return 1


def _print_help():
    """Print help message."""
    print("""
AI Video Editor - Self-contained recipe for PraisonAI

Usage:
  python -m ai_video_editor.cli <command> [options]

Commands:
  edit <input>        Edit video with AI analysis
  probe <input>       Extract video metadata
  transcript <input>  Generate transcript with timestamps
  doctor              Check dependencies
  help                Show this help

Edit Options:
  --output, -o PATH       Output video path
  --preset PRESET         Edit preset (podcast, meeting, course, clean)
  --remove-fillers        Remove filler words (um, uh, like, etc.)
  --remove-repetitions    Remove repeated phrases
  --remove-tangents       Remove off-topic content
  --auto-crop MODE        Crop mode (off, center, face)
  --target-length TIME    Target duration (e.g., 6m, 90s)
  --captions MODE         Caption mode (off, srt, burn)
  --provider PROVIDER     Transcription provider (openai, local, auto)
  --no-llm                Use simple pattern matching instead of LLM
  --force                 Overwrite output if exists
  --json-report PATH      Save JSON report to path
  --verbose, -v           Enable verbose output

Presets:
  podcast   Remove fillers, repetitions, long silences
  meeting   Remove fillers, repetitions, tangents, silences
  course    Remove fillers, repetitions, short silences
  clean     Aggressive removal of all detected issues

Examples:
  python -m ai_video_editor.cli edit input.mp4 --preset podcast --output out.mp4
  python -m ai_video_editor.cli edit input.mp4 --remove-fillers --remove-tangents
  python -m ai_video_editor.cli probe input.mp4
  python -m ai_video_editor.cli transcript input.mp4 --output transcript.srt
  python -m ai_video_editor.cli doctor

Environment Variables:
  OPENAI_API_KEY      Required for transcription and LLM analysis
  WHISPER_MODEL       Local whisper model size (default: small)
  DEBUG               Enable debug output
""")


def cmd_edit(args):
    """Handle edit command."""
    from .pipeline import edit
    
    # Determine overrides from flags
    remove_fillers = True if args.remove_fillers else None
    remove_repetitions = True if args.remove_repetitions else None
    remove_tangents = True if args.remove_tangents else None
    remove_silence = True if args.remove_silence else None
    
    result = edit(
        input_path=args.input,
        output_path=args.output,
        preset=args.preset,
        remove_fillers=remove_fillers,
        remove_repetitions=remove_repetitions,
        remove_tangents=remove_tangents,
        remove_silence=remove_silence,
        auto_crop=args.auto_crop,
        target_length=args.target_length,
        captions=args.captions,
        provider=args.provider,
        use_llm=not args.no_llm,
        force=args.force,
        verbose=args.verbose
    )
    
    # Print summary
    print(f"\n✓ Edit complete!")
    print(f"  Output: {result.output_path}")
    print(f"  Original: {_format_duration(result.original_duration)}")
    print(f"  Final: {_format_duration(result.final_duration)}")
    print(f"  Saved: {_format_duration(result.time_saved)} ({result.time_saved/result.original_duration*100:.1f}%)")
    print(f"\nArtifacts:")
    print(f"  Transcript: {result.transcript_path}")
    print(f"  Captions: {result.srt_path}")
    print(f"  Edit Plan: {result.report_path}")
    print(f"  EDL: {result.edl_path}")
    
    if args.json_report:
        result.to_json(args.json_report)
        print(f"  JSON Report: {args.json_report}")
    
    return 0


def cmd_probe(args):
    """Handle probe command."""
    from .pipeline import probe
    
    result = probe(args.input)
    
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"File: {result.path}")
        print(f"Duration: {_format_duration(result.duration)}")
        print(f"Resolution: {result.width}x{result.height}")
        print(f"FPS: {result.fps}")
        print(f"Video Codec: {result.codec}")
        if result.audio_codec:
            print(f"Audio Codec: {result.audio_codec}")
            print(f"Audio Channels: {result.audio_channels}")
            print(f"Sample Rate: {result.audio_sample_rate} Hz")
        print(f"File Size: {result.file_size / 1024 / 1024:.2f} MB")
    
    return 0


def cmd_transcript(args):
    """Handle transcript command."""
    from .pipeline import transcript
    
    result = transcript(
        input_path=args.input,
        provider=args.provider,
        language=args.language
    )
    
    output_path = args.output
    if output_path is None:
        stem = Path(args.input).stem
        if args.format == "srt":
            output_path = f"{stem}.srt"
        elif args.format == "txt":
            output_path = f"{stem}.txt"
        else:
            output_path = f"{stem}_transcript.json"
    
    if args.format == "srt":
        result.to_srt(output_path)
        print(f"✓ SRT saved to: {output_path}")
    elif args.format == "txt":
        Path(output_path).write_text(result.text)
        print(f"✓ Transcript saved to: {output_path}")
    else:
        Path(output_path).write_text(json.dumps(result.to_dict(), indent=2))
        print(f"✓ JSON saved to: {output_path}")
    
    print(f"  Words: {len(result.words)}")
    print(f"  Duration: {_format_duration(result.duration)}")
    print(f"  Provider: {result.provider}")
    
    return 0


def cmd_doctor(args):
    """Handle doctor command."""
    from .utils import check_ffmpeg, check_ffprobe
    
    print("AI Video Editor - Dependency Check\n")
    
    all_ok = True
    
    # Check FFmpeg
    ffmpeg_ok, ffmpeg_msg = check_ffmpeg()
    if ffmpeg_ok:
        print(f"✓ FFmpeg: {ffmpeg_msg}")
    else:
        print(f"✗ FFmpeg: {ffmpeg_msg}")
        all_ok = False
    
    # Check FFprobe
    ffprobe_ok, ffprobe_msg = check_ffprobe()
    if ffprobe_ok:
        print(f"✓ FFprobe: {ffprobe_msg}")
    else:
        print(f"✗ FFprobe: {ffprobe_msg}")
        all_ok = False
    
    # Check OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print(f"✓ OPENAI_API_KEY: Set ({len(api_key)} chars)")
    else:
        print("✗ OPENAI_API_KEY: Not set")
        all_ok = False
    
    # Check OpenAI package
    try:
        import openai
        print(f"✓ openai package: {openai.__version__}")
    except ImportError:
        print("✗ openai package: Not installed (pip install openai)")
        all_ok = False
    
    # Check faster-whisper (optional)
    try:
        import faster_whisper
        print(f"✓ faster-whisper: Available (optional)")
    except ImportError:
        print("○ faster-whisper: Not installed (optional, for local transcription)")
    
    print()
    if all_ok:
        print("All required dependencies are available!")
        return 0
    else:
        print("Some dependencies are missing. Please install them to use all features.")
        return 1


def _format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    
    return " ".join(parts)


if __name__ == "__main__":
    sys.exit(main())
