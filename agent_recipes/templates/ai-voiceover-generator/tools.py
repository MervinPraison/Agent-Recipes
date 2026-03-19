"""
Tools for ai-voiceover-generator recipe.
Uses AudioAgent for text-to-speech voice generation.
"""

from praisonaiagents import AudioAgent
from praisonaiagents.tools import write_file

_audio_agent = None

def _get_audio_agent():
    global _audio_agent
    if _audio_agent is None:
        _audio_agent = AudioAgent(llm="openai/tts-1")
    return _audio_agent


def generate_speech(text: str, output_path: str = "voiceover.mp3", voice: str = "alloy") -> str:
    """
    Generate speech audio from text.
    
    Args:
        text: Text to convert to speech
        output_path: Output audio file path
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        
    Returns:
        Path to generated audio file
    """
    agent = _get_audio_agent()
    result = agent.speech(text, output=output_path, voice=voice)
    return output_path


def say(text: str, output: str = "output.mp3") -> str:
    """
    Quick TTS - convert text to speech and save.
    
    Args:
        text: Text to speak
        output: Output filename
        
    Returns:
        Path to saved audio file
    """
    agent = _get_audio_agent()
    return agent.say(text, output=output)


def generate_with_emotion(text: str, emotion: str, output_path: str = "voiceover.mp3") -> str:
    """
    Generate voiceover with emotional tone.
    
    Args:
        text: Text to convert
        emotion: Desired emotion (calm, energetic, serious, friendly)
        output_path: Output file path
        
    Returns:
        Path to generated audio
    """
    # Map emotions to appropriate voices
    voice_map = {
        "calm": "shimmer",
        "energetic": "nova",
        "serious": "onyx",
        "friendly": "alloy"
    }
    voice = voice_map.get(emotion.lower(), "alloy")
    
    agent = _get_audio_agent()
    result = agent.speech(text, output=output_path, voice=voice)
    return output_path


TOOLS = [generate_speech, say, generate_with_emotion]


def get_all_tools():
    return TOOLS
