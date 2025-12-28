"""
Audio transcription with word-level timestamps.

Supports:
- OpenAI Whisper API (default, requires OPENAI_API_KEY)
- Local faster-whisper (optional fallback)
"""

import os
from pathlib import Path
from typing import List, Literal

from .models import TranscriptResult, Word
from .utils import extract_audio, create_workdir


def transcript(
    input_path: str,
    provider: Literal["openai", "local", "auto"] = "auto",
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
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if provider == "auto":
        if os.environ.get("OPENAI_API_KEY"):
            provider = "openai"
        else:
            provider = "local"
    
    audio_path = input_path
    input_ext = Path(input_path).suffix.lower()
    
    if input_ext in [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"]:
        if workdir is None:
            work_path = create_workdir(input_path)
        else:
            work_path = Path(workdir)
            work_path.mkdir(parents=True, exist_ok=True)
        
        audio_path = str(work_path / "audio" / "extracted.wav")
        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        extract_audio(input_path, audio_path)
    
    if provider == "openai":
        return _transcribe_openai(audio_path, language)
    elif provider == "local":
        return _transcribe_local(audio_path, language)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _transcribe_openai(audio_path: str, language: str) -> TranscriptResult:
    """Transcribe using OpenAI Whisper API."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "OpenAI package required for transcription. "
            "Install with: pip install openai"
        )
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable required for OpenAI transcription"
        )
    
    client = OpenAI(api_key=api_key)
    
    file_size = os.path.getsize(audio_path)
    if file_size > 25 * 1024 * 1024:
        return _transcribe_openai_chunked(client, audio_path, language)
    
    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=language,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    
    words = []
    if hasattr(response, "words") and response.words:
        for w in response.words:
            words.append(Word(
                text=w.word if hasattr(w, "word") else w.get("word", ""),
                start=w.start if hasattr(w, "start") else w.get("start", 0),
                end=w.end if hasattr(w, "end") else w.get("end", 0),
                confidence=1.0
            ))
    
    duration = words[-1].end if words else 0.0
    
    return TranscriptResult(
        text=response.text if hasattr(response, "text") else str(response),
        words=words,
        language=language,
        duration=duration,
        provider="openai"
    )


def _transcribe_openai_chunked(
    client,
    audio_path: str,
    language: str,
    chunk_duration: int = 600
) -> TranscriptResult:
    """Transcribe long audio by chunking."""
    import subprocess
    import tempfile
    
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True
    )
    total_duration = float(result.stdout.strip())
    
    all_words: List[Word] = []
    all_text_parts: List[str] = []
    
    offset = 0.0
    
    while offset < total_duration:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            chunk_path = tmp.name
        
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(offset),
            "-i", audio_path,
            "-t", str(chunk_duration),
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            chunk_path
        ], capture_output=True)
        
        with open(chunk_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=language,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        
        if hasattr(response, "words") and response.words:
            for w in response.words:
                word_start = (w.start if hasattr(w, "start") else w.get("start", 0)) + offset
                word_end = (w.end if hasattr(w, "end") else w.get("end", 0)) + offset
                all_words.append(Word(
                    text=w.word if hasattr(w, "word") else w.get("word", ""),
                    start=word_start,
                    end=word_end,
                    confidence=1.0
                ))
        
        all_text_parts.append(response.text if hasattr(response, "text") else str(response))
        
        os.unlink(chunk_path)
        offset += chunk_duration
    
    return TranscriptResult(
        text=" ".join(all_text_parts),
        words=all_words,
        language=language,
        duration=total_duration,
        provider="openai"
    )


def _transcribe_local(audio_path: str, language: str) -> TranscriptResult:
    """Transcribe using local faster-whisper."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise ImportError(
            "faster-whisper package required for local transcription. "
            "Install with: pip install faster-whisper"
        )
    
    model_size = os.environ.get("WHISPER_MODEL", "small")
    device = os.environ.get("WHISPER_DEVICE", "auto")
    compute_type = os.environ.get("WHISPER_COMPUTE_TYPE", "auto")
    
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    
    segments, info = model.transcribe(
        audio_path,
        language=language,
        word_timestamps=True
    )
    
    words: List[Word] = []
    text_parts: List[str] = []
    
    for segment in segments:
        text_parts.append(segment.text)
        if segment.words:
            for w in segment.words:
                words.append(Word(
                    text=w.word,
                    start=w.start,
                    end=w.end,
                    confidence=w.probability if hasattr(w, "probability") else 1.0
                ))
    
    duration = words[-1].end if words else 0.0
    
    return TranscriptResult(
        text=" ".join(text_parts),
        words=words,
        language=info.language if hasattr(info, "language") else language,
        duration=duration,
        provider="local"
    )
