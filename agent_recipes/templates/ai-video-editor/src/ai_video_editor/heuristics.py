"""
Heuristic-based content analysis (non-LLM).

Provides fast detection of:
- Filler words
- Repetitions
- Long silences
"""

from typing import List

from .models import Segment, SegmentCategory, TranscriptResult


def detect_fillers(
    transcript: TranscriptResult,
    filler_words: List[str]
) -> List[Segment]:
    """
    Detect filler words in transcript using simple pattern matching.
    
    Args:
        transcript: Transcript with word timestamps
        filler_words: List of filler words to detect
        
    Returns:
        List of segments containing fillers
    """
    filler_segments = []
    filler_set = set(w.lower().strip() for w in filler_words)
    
    for word in transcript.words:
        word_text = word.text.lower().strip().strip(".,!?")
        if word_text in filler_set:
            filler_segments.append(Segment(
                start=word.start,
                end=word.end,
                category=SegmentCategory.FILLER,
                reason=f"Filler word: {word.text}",
                text=word.text
            ))
    
    return filler_segments


def detect_repetitions(
    transcript: TranscriptResult,
    window_size: int = 5,
    min_repeat_words: int = 3
) -> List[Segment]:
    """
    Detect repeated phrases in transcript.
    
    Looks for patterns where speaker restarts or repeats themselves.
    
    Args:
        transcript: Transcript with word timestamps
        window_size: Number of words to look ahead for repetition
        min_repeat_words: Minimum words to consider a repetition
        
    Returns:
        List of segments containing repetitions
    """
    repetition_segments = []
    words = transcript.words
    
    i = 0
    while i < len(words) - min_repeat_words:
        current_phrase = [w.text.lower().strip(".,!?") for w in words[i:i+min_repeat_words]]
        
        for j in range(i + 1, min(i + window_size + 1, len(words) - min_repeat_words + 1)):
            next_phrase = [w.text.lower().strip(".,!?") for w in words[j:j+min_repeat_words]]
            
            if current_phrase == next_phrase:
                repetition_segments.append(Segment(
                    start=words[i].start,
                    end=words[j-1].end if j > i else words[i+min_repeat_words-1].end,
                    category=SegmentCategory.REPEAT,
                    reason=f"Repeated phrase: {' '.join(current_phrase)}",
                    text=" ".join(w.text for w in words[i:j])
                ))
                i = j + min_repeat_words - 1
                break
        
        i += 1
    
    return repetition_segments


def detect_silence(
    transcript: TranscriptResult,
    threshold_ms: float = 700
) -> List[Segment]:
    """
    Detect long silences between words.
    
    Args:
        transcript: Transcript with word timestamps
        threshold_ms: Minimum silence duration in milliseconds
        
    Returns:
        List of segments containing silences
    """
    silence_segments = []
    threshold_s = threshold_ms / 1000.0
    
    words = transcript.words
    for i in range(len(words) - 1):
        gap = words[i + 1].start - words[i].end
        if gap >= threshold_s:
            silence_segments.append(Segment(
                start=words[i].end,
                end=words[i + 1].start,
                category=SegmentCategory.SILENCE,
                reason=f"Silence: {gap:.2f}s",
                text=""
            ))
    
    return silence_segments
