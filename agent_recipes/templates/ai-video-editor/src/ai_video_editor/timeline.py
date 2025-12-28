"""
Timeline optimization for video editing.

Handles:
- Merging overlapping segments
- Snapping to word boundaries
- Applying padding/handles
- Enforcing minimum segment lengths
- Target duration constraints
"""

from typing import Any, Dict, List, Tuple

from .models import EditPlan, Segment, SegmentCategory, TranscriptResult, Word


def optimize_timeline(
    edit_plan: EditPlan,
    transcript: TranscriptResult,
    config: Dict[str, Any]
) -> EditPlan:
    """
    Optimize edit plan timeline.
    
    Args:
        edit_plan: Initial edit plan
        transcript: Transcript with word timestamps
        config: Configuration with padding, min_segment_length, etc.
        
    Returns:
        Optimized EditPlan
    """
    padding_ms = config.get("padding_ms", 120)
    padding_s = padding_ms / 1000.0
    min_segment_length = config.get("min_segment_length", 1.2)
    target_length = config.get("target_length")
    
    segments_to_keep = [
        _snap_to_word_boundaries(seg, transcript.words)
        for seg in edit_plan.segments_to_keep
    ]
    
    segments_to_remove = [
        _snap_to_word_boundaries(seg, transcript.words)
        for seg in edit_plan.segments_to_remove
    ]
    
    segments_to_keep = _merge_overlapping(segments_to_keep)
    
    segments_to_keep = _apply_padding(
        segments_to_keep,
        padding_s,
        0.0,
        transcript.duration
    )
    
    segments_to_keep = [
        seg for seg in segments_to_keep
        if seg.duration >= min_segment_length
    ]
    
    segments_to_remove = _calculate_remove_segments(
        segments_to_keep,
        edit_plan.segments_to_remove,
        transcript.duration
    )
    
    if target_length:
        segments_to_keep = _apply_target_length(
            segments_to_keep,
            segments_to_remove,
            target_length
        )
    
    return EditPlan(
        segments_to_keep=segments_to_keep,
        segments_to_remove=segments_to_remove,
        chapters=edit_plan.chapters,
        summary=edit_plan.summary,
        topics=edit_plan.topics
    )


def _snap_to_word_boundaries(segment: Segment, words: List[Word]) -> Segment:
    """Snap segment boundaries to nearest word boundaries."""
    if not words:
        return segment
    
    new_start = segment.start
    for word in words:
        if word.start >= segment.start:
            new_start = word.start
            break
        if word.end >= segment.start:
            new_start = word.start
            break
    
    new_end = segment.end
    for word in reversed(words):
        if word.end <= segment.end:
            new_end = word.end
            break
        if word.start <= segment.end:
            new_end = word.end
            break
    
    if new_end <= new_start:
        return segment
    
    return Segment(
        start=new_start,
        end=new_end,
        category=segment.category,
        reason=segment.reason,
        confidence=segment.confidence,
        text=segment.text,
        words=segment.words
    )


def _merge_overlapping(segments: List[Segment]) -> List[Segment]:
    """Merge overlapping or adjacent segments."""
    if not segments:
        return []
    
    sorted_segs = sorted(segments, key=lambda s: s.start)
    merged = [sorted_segs[0]]
    
    for seg in sorted_segs[1:]:
        last = merged[-1]
        
        if seg.start <= last.end + 0.1:
            merged[-1] = Segment(
                start=last.start,
                end=max(last.end, seg.end),
                category=last.category,
                reason=f"{last.reason}; {seg.reason}" if seg.reason else last.reason,
                text=f"{last.text} {seg.text}".strip()
            )
        else:
            merged.append(seg)
    
    return merged


def _apply_padding(
    segments: List[Segment],
    padding_s: float,
    min_time: float,
    max_time: float
) -> List[Segment]:
    """Apply padding/handles to segment boundaries."""
    padded = []
    
    for seg in segments:
        new_start = max(min_time, seg.start - padding_s)
        new_end = min(max_time, seg.end + padding_s)
        
        padded.append(Segment(
            start=new_start,
            end=new_end,
            category=seg.category,
            reason=seg.reason,
            text=seg.text
        ))
    
    return _merge_overlapping(padded)


def _calculate_remove_segments(
    keep_segments: List[Segment],
    original_remove: List[Segment],
    total_duration: float
) -> List[Segment]:
    """Calculate remove segments as gaps between keep segments."""
    if not keep_segments:
        return original_remove
    
    remove_segments = []
    sorted_keep = sorted(keep_segments, key=lambda s: s.start)
    
    if sorted_keep[0].start > 0.01:
        reason = _find_remove_reason(0, sorted_keep[0].start, original_remove)
        category = _find_remove_category(0, sorted_keep[0].start, original_remove)
        remove_segments.append(Segment(
            start=0,
            end=sorted_keep[0].start,
            category=category,
            reason=reason
        ))
    
    for i in range(len(sorted_keep) - 1):
        gap_start = sorted_keep[i].end
        gap_end = sorted_keep[i + 1].start
        
        if gap_end - gap_start > 0.01:
            reason = _find_remove_reason(gap_start, gap_end, original_remove)
            category = _find_remove_category(gap_start, gap_end, original_remove)
            remove_segments.append(Segment(
                start=gap_start,
                end=gap_end,
                category=category,
                reason=reason
            ))
    
    if sorted_keep[-1].end < total_duration - 0.01:
        reason = _find_remove_reason(sorted_keep[-1].end, total_duration, original_remove)
        category = _find_remove_category(sorted_keep[-1].end, total_duration, original_remove)
        remove_segments.append(Segment(
            start=sorted_keep[-1].end,
            end=total_duration,
            category=category,
            reason=reason
        ))
    
    return remove_segments


def _find_remove_reason(start: float, end: float, original_remove: List[Segment]) -> str:
    """Find reason for removal from original segments."""
    for seg in original_remove:
        if seg.start < end and seg.end > start:
            return seg.reason
    return "Removed"


def _find_remove_category(start: float, end: float, original_remove: List[Segment]) -> SegmentCategory:
    """Find category for removal from original segments."""
    for seg in original_remove:
        if seg.start < end and seg.end > start:
            return seg.category
    return SegmentCategory.FILLER


def _apply_target_length(
    keep_segments: List[Segment],
    remove_segments: List[Segment],
    target_length: float
) -> List[Segment]:
    """Adjust segments to meet target length."""
    current_duration = sum(s.duration for s in keep_segments)
    
    if current_duration <= target_length:
        return keep_segments
    
    excess = current_duration - target_length
    sorted_segs = sorted(keep_segments, key=lambda s: s.confidence)
    
    result = []
    removed_duration = 0.0
    
    for seg in sorted_segs:
        if removed_duration < excess and seg.duration < excess - removed_duration:
            removed_duration += seg.duration
        else:
            result.append(seg)
    
    return sorted(result, key=lambda s: s.start)


def get_keep_intervals(edit_plan: EditPlan) -> List[Tuple[float, float]]:
    """Get list of (start, end) tuples for segments to keep."""
    intervals = [(seg.start, seg.end) for seg in edit_plan.segments_to_keep]
    return sorted(intervals, key=lambda x: x[0])


def get_remove_intervals(edit_plan: EditPlan) -> List[Tuple[float, float, str]]:
    """Get list of (start, end, reason) tuples for segments to remove."""
    intervals = [
        (seg.start, seg.end, seg.reason)
        for seg in edit_plan.segments_to_remove
    ]
    return sorted(intervals, key=lambda x: x[0])


def calculate_final_duration(edit_plan: EditPlan) -> float:
    """Calculate final video duration after edits."""
    return sum(seg.duration for seg in edit_plan.segments_to_keep)
