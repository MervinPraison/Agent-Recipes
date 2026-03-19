"""
Tools for ai-speech-to-text recipe.
Uses AudioAgent for high-quality speech transcription.
"""

from praisonaiagents import AudioAgent

_audio_agent = None

def _get_audio_agent():
    global _audio_agent
    if _audio_agent is None:
        _audio_agent = AudioAgent(llm="openai/whisper-1")
    return _audio_agent


def transcribe_audio(audio_path: str, language: str = "en") -> str:
    """
    Transcribe speech from audio file.
    
    Args:
        audio_path: Path to audio file
        language: Language code (e.g., 'en', 'es', 'fr')
        
    Returns:
        Transcribed text
    """
    agent = _get_audio_agent()
    result = agent.transcribe(audio_path, language=language)
    return result.text if hasattr(result, 'text') else str(result)


def listen(audio_path: str) -> str:
    """
    Quick transcription of audio file.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Transcribed text
    """
    agent = _get_audio_agent()
    return agent.listen(audio_path)


TOOLS = [transcribe_audio, listen]


def get_all_tools():
    return TOOLS
