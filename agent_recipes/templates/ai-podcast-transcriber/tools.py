"""
Tools for ai-podcast-transcriber recipe.
Uses AudioAgent for high-quality podcast transcription.
"""

from praisonaiagents import AudioAgent
from praisonaiagents.tools import execute_command, write_file
import os

_audio_agent = None

def _get_audio_agent():
    global _audio_agent
    if _audio_agent is None:
        _audio_agent = AudioAgent(llm="openai/whisper-1")
    return _audio_agent


def transcribe_podcast(audio_path: str, language: str = "en") -> str:
    """
    Transcribe a podcast episode with high accuracy.
    
    Args:
        audio_path: Path to podcast audio file
        language: Language code
        
    Returns:
        Full transcription text
    """
    agent = _get_audio_agent()
    result = agent.transcribe(audio_path, language=language)
    return result.text if hasattr(result, 'text') else str(result)


def get_audio_duration(audio_path: str) -> str:
    """
    Get the duration of an audio file.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    result = execute_command(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '{audio_path}'")
    return result.get("stdout", "Unknown").strip()


def split_audio_by_silence(audio_path: str, output_dir: str = "segments") -> str:
    """
    Split audio file by silence (for chapter detection).
    
    Args:
        audio_path: Path to audio file
        output_dir: Directory for output segments
        
    Returns:
        List of segment file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    result = execute_command(
        f"ffmpeg -i '{audio_path}' -af silencedetect=noise=-30dB:d=2 -f null - 2>&1 | grep silence_end"
    )
    return result.get("stdout", "No silence detected")


def save_transcript(text: str, output_path: str = "transcript.txt") -> str:
    """
    Save transcription to file.
    
    Args:
        text: Transcription text
        output_path: Output file path
        
    Returns:
        Path to saved file
    """
    write_file(output_path, text)
    return output_path


TOOLS = [transcribe_podcast, get_audio_duration, split_audio_by_silence, save_transcript]


def get_all_tools():
    return TOOLS
