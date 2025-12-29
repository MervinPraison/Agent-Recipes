"""
AI Voiceover Generator Tools

Generate voice overs using TTS:
- OpenAI TTS
- Multiple voices
- Speed control
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def generate_voiceover(
    text: str,
    output_path: Optional[str] = None,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0,
) -> Dict[str, Any]:
    """
    Generate voiceover from text using OpenAI TTS.
    
    Args:
        text: Text to convert to speech
        output_path: Output audio file path
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        model: TTS model (tts-1, tts-1-hd)
        speed: Speech speed (0.25 to 4.0)
        
    Returns:
        Dictionary with audio info
    """
    import requests
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY not set"}
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"voiceover_{timestamp}.mp3"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "input": text,
                "voice": voice,
                "speed": speed,
            },
            timeout=120,
        )
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return {
            "path": output_path,
            "voice": voice,
            "model": model,
            "text_length": len(text),
            "size_bytes": len(response.content),
        }
        
    except Exception as e:
        logger.error(f"Error generating voiceover: {e}")
        return {"error": str(e)}


def generate_speech(
    script: str,
    output_dir: Optional[str] = None,
    voice: str = "alloy",
    chunk_size: int = 4000,
) -> Dict[str, Any]:
    """
    Generate speech from a longer script, chunking if needed.
    
    Args:
        script: Full script text
        output_dir: Output directory
        voice: Voice to use
        chunk_size: Max characters per chunk
        
    Returns:
        Dictionary with audio files
    """
    output_dir = output_dir or "./voiceovers"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Split into chunks if needed
    chunks = []
    if len(script) > chunk_size:
        words = script.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
    else:
        chunks = [script]
    
    audio_files = []
    
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(output_dir, f"speech_{i:03d}.mp3")
        result = generate_voiceover(chunk, output_path, voice)
        
        if "path" in result:
            audio_files.append(result["path"])
        else:
            logger.warning(f"Error generating chunk {i}: {result.get('error')}")
    
    # Concatenate if multiple files
    if len(audio_files) > 1:
        final_path = os.path.join(output_dir, "speech_full.mp3")
        concat_audio(audio_files, final_path)
        return {
            "path": final_path,
            "chunks": len(audio_files),
            "chunk_files": audio_files,
        }
    elif audio_files:
        return {
            "path": audio_files[0],
            "chunks": 1,
        }
    else:
        return {"error": "No audio generated"}


def concat_audio(
    audio_files: list,
    output_path: str,
) -> Dict[str, Any]:
    """
    Concatenate multiple audio files.
    
    Args:
        audio_files: List of audio file paths
        output_path: Output file path
        
    Returns:
        Dictionary with output info
    """
    import subprocess
    import tempfile
    
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            for audio in audio_files:
                f.write(f"file '{audio}'\n")
            concat_file = f.name
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        os.unlink(concat_file)
        
        return {"path": output_path}
        
    except Exception as e:
        logger.error(f"Error concatenating audio: {e}")
        return {"error": str(e)}
