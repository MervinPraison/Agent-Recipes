"""
Tools for ai-subtitle-generator recipe.
Uses AudioAgent for transcription with timestamps.
"""

from praisonaiagents import AudioAgent
from praisonaiagents.tools import execute_command

_audio_agent = None

def _get_audio_agent():
    global _audio_agent
    if _audio_agent is None:
        _audio_agent = AudioAgent(llm="openai/whisper-1")
    return _audio_agent


def transcribe_audio(audio_path: str, language: str = "en") -> str:
    """
    Transcribe audio file with timestamps for subtitle generation.
    
    Args:
        audio_path: Path to audio/video file
        language: Language code (e.g., 'en', 'es', 'fr')
        
    Returns:
        Transcription text with timing information
    """
    agent = _get_audio_agent()
    result = agent.transcribe(audio_path, language=language)
    return result.text if hasattr(result, 'text') else str(result)


def extract_audio_from_video(video_path: str, output_path: str = "extracted_audio.mp3") -> str:
    """
    Extract audio track from video file using ffmpeg.
    
    Args:
        video_path: Path to video file
        output_path: Output audio file path
        
    Returns:
        Path to extracted audio file
    """
    result = execute_command(f"ffmpeg -y -i '{video_path}' -vn -acodec mp3 '{output_path}'")
    if result.get("return_code", 1) == 0:
        return output_path
    return f"Error: {result.get('stderr', 'Failed to extract audio')}"


def format_as_srt(transcription: str, output_path: str = "subtitles.srt") -> str:
    """
    Format transcription as SRT subtitle file.
    
    Args:
        transcription: Raw transcription text
        output_path: Output SRT file path
        
    Returns:
        Path to generated SRT file
    """
    # This is a placeholder - actual implementation would parse timestamps
    # from whisper verbose output and format as SRT
    lines = transcription.split('\n')
    srt_lines = []
    for i, line in enumerate(lines, 1):
        if line.strip():
            # Estimate timing (in real impl, use actual timestamps)
            start = f"00:00:{(i-1)*5:02d},000"
            end = f"00:00:{i*5:02d},000"
            srt_lines.append(f"{i}\n{start} --> {end}\n{line.strip()}\n")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(srt_lines))
    
    return output_path


TOOLS = [transcribe_audio, extract_audio_from_video, format_as_srt]


def get_all_tools():
    return TOOLS
