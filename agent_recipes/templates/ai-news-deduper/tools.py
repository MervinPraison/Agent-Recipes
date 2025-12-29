"""
AI News Deduper Tools

Tools for deduplicating and clustering news articles:
- Semantic similarity detection
- Topic clustering
- Duplicate removal
"""

import hashlib
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def get_text_hash(text: str) -> str:
    """Generate a hash for text content."""
    return hashlib.md5(text.lower().strip().encode()).hexdigest()


def get_embedding(text: str) -> List[float]:
    """Get embedding for text using OpenAI API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    
    import requests
    
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "text-embedding-3-small",
            "input": text[:8000],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    import math
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def deduplicate_articles(
    articles: List[Dict[str, Any]],
    similarity_threshold: float = 0.85,
    use_semantic: bool = True,
) -> Dict[str, Any]:
    """
    Deduplicate articles based on title and content similarity.
    
    Args:
        articles: List of article dictionaries
        similarity_threshold: Threshold for considering articles as duplicates
        use_semantic: Use semantic similarity (requires API) or hash-based
        
    Returns:
        Dictionary with deduplicated articles and stats
    """
    if not articles:
        return {"deduplicated": [], "removed": 0, "stats": {}}
    
    seen_hashes = set()
    deduplicated = []
    removed_count = 0
    
    if use_semantic:
        # Get embeddings for all articles
        embeddings = []
        for article in articles:
            text = f"{article.get('title', '')} {article.get('content', '')[:500]}"
            try:
                embedding = get_embedding(text)
                embeddings.append(embedding)
            except Exception as e:
                logger.warning(f"Error getting embedding: {e}")
                embeddings.append(None)
        
        # Check for duplicates using cosine similarity
        for i, article in enumerate(articles):
            is_duplicate = False
            
            if embeddings[i] is not None:
                for j in range(len(deduplicated)):
                    if embeddings[j] is not None:
                        sim = cosine_similarity(embeddings[i], embeddings[j])
                        if sim >= similarity_threshold:
                            is_duplicate = True
                            break
            
            if not is_duplicate:
                deduplicated.append(article)
            else:
                removed_count += 1
    else:
        # Hash-based deduplication
        for article in articles:
            title_hash = get_text_hash(article.get("title", ""))
            if title_hash not in seen_hashes:
                seen_hashes.add(title_hash)
                deduplicated.append(article)
            else:
                removed_count += 1
    
    return {
        "deduplicated": deduplicated,
        "removed": removed_count,
        "stats": {
            "original_count": len(articles),
            "final_count": len(deduplicated),
            "duplicate_rate": removed_count / len(articles) if articles else 0,
        }
    }


def cluster_by_topic(
    articles: List[Dict[str, Any]],
    min_cluster_size: int = 2,
    num_clusters: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Cluster articles by topic using semantic similarity.
    
    Args:
        articles: List of article dictionaries
        min_cluster_size: Minimum articles per cluster
        num_clusters: Number of clusters (auto-detected if None)
        
    Returns:
        Dictionary with clusters and unclustered articles
    """
    if len(articles) < 2:
        return {"clusters": [], "unclustered": articles}
    
    # Get embeddings
    embeddings = []
    valid_articles = []
    
    for article in articles:
        text = f"{article.get('title', '')} {article.get('content', '')[:500]}"
        try:
            embedding = get_embedding(text)
            embeddings.append(embedding)
            valid_articles.append(article)
        except Exception as e:
            logger.warning(f"Error getting embedding: {e}")
    
    if len(embeddings) < 2:
        return {"clusters": [], "unclustered": articles}
    
    # Simple clustering: group articles with high similarity
    clusters = []
    used = set()
    
    for i in range(len(valid_articles)):
        if i in used:
            continue
        
        cluster = [valid_articles[i]]
        used.add(i)
        
        for j in range(i + 1, len(valid_articles)):
            if j in used:
                continue
            
            sim = cosine_similarity(embeddings[i], embeddings[j])
            if sim >= 0.7:  # Cluster threshold
                cluster.append(valid_articles[j])
                used.add(j)
        
        if len(cluster) >= min_cluster_size:
            # Generate cluster topic from titles
            titles = [a.get("title", "") for a in cluster]
            clusters.append({
                "topic": _extract_common_topic(titles),
                "articles": cluster,
                "size": len(cluster),
            })
    
    # Collect unclustered articles
    unclustered = [a for i, a in enumerate(valid_articles) if i not in used]
    
    return {
        "clusters": clusters,
        "unclustered": unclustered,
        "stats": {
            "num_clusters": len(clusters),
            "clustered_articles": sum(c["size"] for c in clusters),
            "unclustered_articles": len(unclustered),
        }
    }


def _extract_common_topic(titles: List[str]) -> str:
    """Extract common topic from a list of titles."""
    if not titles:
        return "Unknown Topic"
    
    # Simple approach: find common words
    word_counts = {}
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                  "have", "has", "had", "do", "does", "did", "will", "would", "could",
                  "should", "may", "might", "must", "shall", "can", "to", "of", "in",
                  "for", "on", "with", "at", "by", "from", "as", "into", "through",
                  "and", "or", "but", "if", "then", "else", "when", "where", "why",
                  "how", "all", "each", "every", "both", "few", "more", "most", "other",
                  "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                  "than", "too", "very", "just", "also", "now", "new", "first", "last"}
    
    for title in titles:
        words = title.lower().split()
        for word in words:
            word = word.strip(".,!?:;\"'()[]{}").lower()
            if len(word) > 2 and word not in stop_words:
                word_counts[word] = word_counts.get(word, 0) + 1
    
    # Get top words
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    top_words = [w[0].title() for w in sorted_words[:3]]
    
    return " ".join(top_words) if top_words else "Mixed Topics"
