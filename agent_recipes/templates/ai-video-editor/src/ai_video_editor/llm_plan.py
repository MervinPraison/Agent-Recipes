"""
LLM-based content analysis for video editing.

Uses LLM to:
- Understand video content
- Identify tangent segments
- Generate chapter markers
- Create edit plans
"""

import json
import os
from typing import Any, Dict, List

from .models import (
    Chapter,
    EditPlan,
    Segment,
    SegmentCategory,
    TranscriptResult,
)
from .heuristics import detect_fillers, detect_repetitions, detect_silence


ANALYSIS_SYSTEM_PROMPT = """You are an expert video editor AI assistant. Your task is to analyze video transcripts and create precise edit plans.

You will receive:
1. A transcript with word-level timestamps
2. Configuration for what to remove (fillers, tangents, repetitions)
3. Optional target duration

Your job is to identify segments to KEEP and segments to REMOVE, with precise timestamps.

Rules:
- Never cut in the middle of a word - use word boundaries
- Minimum segment length should be respected
- Add padding around cuts for smooth transitions
- Be conservative with tangent detection - only remove clearly off-topic content
- For fillers, only remove standalone filler words, not fillers that are part of natural speech flow
- For repetitions, identify when speaker restarts a sentence or repeats themselves

Output must be valid JSON matching the specified schema."""


ANALYSIS_USER_PROMPT = """Analyze this transcript and create an edit plan.

TRANSCRIPT:
{transcript}

WORD TIMESTAMPS:
{word_timestamps}

CONFIGURATION:
- Remove fillers: {remove_fillers}
- Filler words to detect: {filler_words}
- Remove repetitions: {remove_repetitions}
- Remove tangents: {remove_tangents}
- Remove long silences: {remove_silence}
- Silence threshold: {silence_threshold_ms}ms
- Minimum segment length: {min_segment_length}s
- Padding around cuts: {padding_ms}ms
{target_length_instruction}

Analyze the content and return a JSON object with this exact structure:
{{
    "summary": "Brief summary of what the video is about",
    "topics": ["main topic 1", "main topic 2"],
    "segments_to_keep": [
        {{"start": 0.0, "end": 10.5, "reason": "Introduction", "text": "transcript text..."}}
    ],
    "segments_to_remove": [
        {{"start": 10.5, "end": 11.2, "category": "filler", "reason": "um", "text": "um"}}
    ],
    "chapters": [
        {{"start": 0.0, "title": "Introduction", "description": "..."}}
    ]
}}

Categories for segments_to_remove: "filler", "tangent", "repeat", "silence"

Be precise with timestamps. Ensure segments don't overlap and cover the entire duration."""


def analyze_content(
    transcript: TranscriptResult,
    config: Dict[str, Any],
    model: str = None
) -> EditPlan:
    """
    Analyze transcript content using LLM.
    
    Args:
        transcript: Transcript with word timestamps
        config: Edit configuration
        model: LLM model to use (default: gpt-4o-mini)
        
    Returns:
        EditPlan with segments to keep/remove
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "OpenAI package required for content analysis. "
            "Install with: pip install openai"
        )
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable required")
    
    client = OpenAI(api_key=api_key)
    
    if model is None:
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    
    word_ts_lines = []
    for w in transcript.words[:500]:
        word_ts_lines.append(f"[{w.start:.2f}-{w.end:.2f}] {w.text}")
    
    target_instruction = ""
    if config.get("target_length"):
        target_instruction = f"- Target output length: {config['target_length']}s (prioritize removing lower-value content to meet this)"
    
    user_prompt = ANALYSIS_USER_PROMPT.format(
        transcript=transcript.text[:8000],
        word_timestamps="\n".join(word_ts_lines),
        remove_fillers=config.get("remove_fillers", True),
        filler_words=", ".join(config.get("filler_words", ["um", "uh"])),
        remove_repetitions=config.get("remove_repetitions", True),
        remove_tangents=config.get("remove_tangents", False),
        remove_silence=config.get("remove_silence", True),
        silence_threshold_ms=config.get("silence_threshold_ms", 700),
        min_segment_length=config.get("min_segment_length", 1.2),
        padding_ms=config.get("padding_ms", 120),
        target_length_instruction=target_instruction
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse LLM response as JSON: {e}\nResponse: {content[:500]}")
    
    return _parse_edit_plan(data)


def _parse_edit_plan(data: Dict[str, Any]) -> EditPlan:
    """Parse LLM response into EditPlan."""
    segments_to_keep = []
    segments_to_remove = []
    chapters = []
    
    for seg_data in data.get("segments_to_keep", []):
        segments_to_keep.append(Segment(
            start=float(seg_data.get("start", 0)),
            end=float(seg_data.get("end", 0)),
            category=SegmentCategory.KEEP,
            reason=seg_data.get("reason", ""),
            text=seg_data.get("text", "")
        ))
    
    for seg_data in data.get("segments_to_remove", []):
        category_str = seg_data.get("category", "filler").lower()
        try:
            category = SegmentCategory(category_str)
        except ValueError:
            category = SegmentCategory.FILLER
        
        segments_to_remove.append(Segment(
            start=float(seg_data.get("start", 0)),
            end=float(seg_data.get("end", 0)),
            category=category,
            reason=seg_data.get("reason", ""),
            text=seg_data.get("text", "")
        ))
    
    for ch_data in data.get("chapters", []):
        chapters.append(Chapter(
            start=float(ch_data.get("start", 0)),
            title=ch_data.get("title", ""),
            description=ch_data.get("description", "")
        ))
    
    return EditPlan(
        segments_to_keep=segments_to_keep,
        segments_to_remove=segments_to_remove,
        chapters=chapters,
        summary=data.get("summary", ""),
        topics=data.get("topics", [])
    )


def create_simple_edit_plan(
    transcript: TranscriptResult,
    config: Dict[str, Any]
) -> EditPlan:
    """
    Create edit plan using simple pattern matching (no LLM).
    
    This is faster but less accurate than LLM-based analysis.
    
    Args:
        transcript: Transcript with word timestamps
        config: Edit configuration
        
    Returns:
        EditPlan with segments to keep/remove
    """
    segments_to_remove = []
    
    if config.get("remove_fillers", True):
        filler_words = config.get("filler_words", ["um", "uh"])
        segments_to_remove.extend(detect_fillers(transcript, filler_words))
    
    if config.get("remove_repetitions", True):
        segments_to_remove.extend(detect_repetitions(transcript))
    
    if config.get("remove_silence", True):
        threshold = config.get("silence_threshold_ms", 700)
        segments_to_remove.extend(detect_silence(transcript, threshold))
    
    segments_to_remove.sort(key=lambda s: s.start)
    
    segments_to_keep = _invert_segments(
        segments_to_remove,
        0.0,
        transcript.duration
    )
    
    return EditPlan(
        segments_to_keep=segments_to_keep,
        segments_to_remove=segments_to_remove,
        summary="",
        topics=[]
    )


def _invert_segments(
    remove_segments: List[Segment],
    start: float,
    end: float
) -> List[Segment]:
    """Convert remove segments to keep segments."""
    if not remove_segments:
        return [Segment(start=start, end=end, category=SegmentCategory.KEEP)]
    
    keep_segments = []
    current = start
    
    for seg in sorted(remove_segments, key=lambda s: s.start):
        if seg.start > current:
            keep_segments.append(Segment(
                start=current,
                end=seg.start,
                category=SegmentCategory.KEEP
            ))
        current = max(current, seg.end)
    
    if current < end:
        keep_segments.append(Segment(
            start=current,
            end=end,
            category=SegmentCategory.KEEP
        ))
    
    return keep_segments
