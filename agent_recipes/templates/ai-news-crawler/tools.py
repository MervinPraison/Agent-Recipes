"""
AI News Crawler Tools

Tools for crawling AI news from multiple sources:
- HackerNews
- Reddit (r/MachineLearning, r/artificial, etc.)
- arXiv (cs.AI, cs.LG, cs.CL)
- GitHub Trending
- AI Labs Blogs
- Web Search (via Tavily)
"""

import json
import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


def crawl_hackernews(
    max_articles: int = 20,
    time_window_hours: int = 24,
    keywords: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Crawl HackerNews for AI-related stories.
    
    Args:
        max_articles: Maximum number of articles to fetch
        time_window_hours: Only fetch articles from the last N hours
        keywords: Filter by keywords (default: AI-related terms)
        
    Returns:
        List of article dictionaries
    """
    import requests
    
    keywords = keywords or ["ai", "gpt", "llm", "machine learning", "openai", "anthropic", "google ai", "neural", "transformer"]
    
    articles = []
    base_url = "https://hacker-news.firebaseio.com/v0"
    
    try:
        # Get top stories
        response = requests.get(f"{base_url}/topstories.json", timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:100]  # Get top 100 to filter
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=time_window_hours)
        
        for story_id in story_ids:
            if len(articles) >= max_articles:
                break
                
            try:
                story_response = requests.get(f"{base_url}/item/{story_id}.json", timeout=5)
                story = story_response.json()
                
                if not story or story.get("type") != "story":
                    continue
                
                title = story.get("title", "").lower()
                
                # Check if AI-related
                if not any(kw in title for kw in keywords):
                    continue
                
                # Check time window
                story_time = datetime.fromtimestamp(story.get("time", 0), tz=timezone.utc)
                if story_time < cutoff_time:
                    continue
                
                articles.append({
                    "title": story.get("title", ""),
                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "source": "hackernews",
                    "published": story_time.isoformat(),
                    "score": story.get("score", 0),
                    "comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "content": "",  # HN doesn't provide content
                })
            except Exception as e:
                logger.warning(f"Error fetching story {story_id}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error crawling HackerNews: {e}")
    
    return articles


def crawl_reddit(
    subreddits: Optional[List[str]] = None,
    max_articles: int = 20,
    time_window_hours: int = 24,
) -> List[Dict[str, Any]]:
    """
    Crawl Reddit for AI-related posts.
    
    Args:
        subreddits: List of subreddits to crawl
        max_articles: Maximum number of articles to fetch
        time_window_hours: Only fetch articles from the last N hours
        
    Returns:
        List of article dictionaries
    """
    import requests
    
    subreddits = subreddits or ["MachineLearning", "artificial", "LocalLLaMA", "OpenAI", "ClaudeAI"]
    articles = []
    
    headers = {"User-Agent": "PraisonAI News Crawler 1.0"}
    
    for subreddit in subreddits:
        if len(articles) >= max_articles:
            break
            
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=time_window_hours)
            
            for post in data.get("data", {}).get("children", []):
                if len(articles) >= max_articles:
                    break
                    
                post_data = post.get("data", {})
                
                # Check time window
                created = datetime.fromtimestamp(post_data.get("created_utc", 0), tz=timezone.utc)
                if created < cutoff_time:
                    continue
                
                articles.append({
                    "title": post_data.get("title", ""),
                    "url": post_data.get("url", ""),
                    "source": f"reddit/r/{subreddit}",
                    "published": created.isoformat(),
                    "score": post_data.get("score", 0),
                    "comments": post_data.get("num_comments", 0),
                    "author": post_data.get("author", ""),
                    "content": post_data.get("selftext", "")[:500],
                })
                
        except Exception as e:
            logger.warning(f"Error crawling r/{subreddit}: {e}")
            continue
    
    return articles


def crawl_arxiv(
    categories: Optional[List[str]] = None,
    max_articles: int = 20,
    time_window_hours: int = 48,
) -> List[Dict[str, Any]]:
    """
    Crawl arXiv for AI research papers.
    
    Args:
        categories: arXiv categories to search
        max_articles: Maximum number of papers to fetch
        time_window_hours: Only fetch papers from the last N hours
        
    Returns:
        List of paper dictionaries
    """
    import requests
    import xml.etree.ElementTree as ET
    
    categories = categories or ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.NE"]
    articles = []
    
    try:
        # Build query
        cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
        url = f"http://export.arxiv.org/api/query?search_query={cat_query}&sortBy=submittedDate&sortOrder=descending&max_results={max_articles}"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            published = entry.find("atom:published", ns)
            link = entry.find("atom:id", ns)
            authors = entry.findall("atom:author/atom:name", ns)
            
            articles.append({
                "title": title.text.strip() if title is not None else "",
                "url": link.text if link is not None else "",
                "source": "arxiv",
                "published": published.text if published is not None else "",
                "content": summary.text.strip()[:500] if summary is not None else "",
                "authors": [a.text for a in authors],
                "score": 0,
            })
            
    except Exception as e:
        logger.error(f"Error crawling arXiv: {e}")
    
    return articles


def crawl_github_trending(
    language: Optional[str] = None,
    max_repos: int = 20,
) -> List[Dict[str, Any]]:
    """
    Crawl GitHub trending repositories for AI projects.
    
    Args:
        language: Filter by programming language
        max_repos: Maximum number of repos to fetch
        
    Returns:
        List of repository dictionaries
    """
    import requests
    from bs4 import BeautifulSoup
    
    articles = []
    
    try:
        url = "https://github.com/trending"
        if language:
            url += f"/{language}"
        url += "?since=daily"
        
        headers = {"User-Agent": "PraisonAI News Crawler 1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # AI-related keywords
        ai_keywords = ["ai", "llm", "gpt", "transformer", "neural", "ml", "machine-learning", 
                       "deep-learning", "nlp", "vision", "agent", "rag", "embedding"]
        
        for article in soup.select("article.Box-row")[:max_repos * 2]:
            try:
                repo_link = article.select_one("h2 a")
                if not repo_link:
                    continue
                    
                repo_name = repo_link.get_text(strip=True).replace("\n", "").replace(" ", "")
                repo_url = "https://github.com" + repo_link.get("href", "")
                
                description_elem = article.select_one("p")
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                # Check if AI-related
                text_to_check = (repo_name + " " + description).lower()
                if not any(kw in text_to_check for kw in ai_keywords):
                    continue
                
                stars_elem = article.select_one("a[href*='/stargazers']")
                stars = stars_elem.get_text(strip=True).replace(",", "") if stars_elem else "0"
                
                articles.append({
                    "title": repo_name,
                    "url": repo_url,
                    "source": "github_trending",
                    "published": datetime.now(timezone.utc).isoformat(),
                    "content": description,
                    "score": int(stars) if stars.isdigit() else 0,
                })
                
                if len(articles) >= max_repos:
                    break
                    
            except Exception as e:
                logger.warning(f"Error parsing repo: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error crawling GitHub trending: {e}")
    
    return articles


def search_web(
    query: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search the web for AI news using Tavily API.
    
    Args:
        query: Search query
        max_results: Maximum number of results
        
    Returns:
        List of search result dictionaries
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        logger.warning("TAVILY_API_KEY not set, skipping web search")
        return []
    
    import requests
    
    articles = []
    
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "search_depth": "advanced",
                "max_results": max_results,
                "include_answer": False,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        
        for result in data.get("results", []):
            articles.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "source": "web_search",
                "published": datetime.now(timezone.utc).isoformat(),
                "content": result.get("content", "")[:500],
                "score": result.get("score", 0),
            })
            
    except Exception as e:
        logger.error(f"Error in web search: {e}")
    
    return articles


def crawl_ai_news(
    sources: Optional[List[str]] = None,
    max_articles: int = 50,
    time_window_hours: int = 24,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main function to crawl AI news from all configured sources.
    
    Args:
        sources: List of sources to crawl
        max_articles: Maximum total articles
        time_window_hours: Time window for articles
        output_dir: Optional directory to save results
        
    Returns:
        Dictionary with articles and metadata
    """
    sources = sources or ["hackernews", "reddit", "arxiv", "github_trending"]
    all_articles = []
    sources_crawled = []
    
    per_source_limit = max(5, max_articles // len(sources))
    
    for source in sources:
        try:
            if source == "hackernews":
                articles = crawl_hackernews(max_articles=per_source_limit, time_window_hours=time_window_hours)
            elif source == "reddit":
                articles = crawl_reddit(max_articles=per_source_limit, time_window_hours=time_window_hours)
            elif source == "arxiv":
                articles = crawl_arxiv(max_articles=per_source_limit, time_window_hours=time_window_hours)
            elif source == "github_trending":
                articles = crawl_github_trending(max_repos=per_source_limit)
            elif source == "web_search":
                articles = search_web("AI news today", max_results=per_source_limit)
            else:
                logger.warning(f"Unknown source: {source}")
                continue
            
            all_articles.extend(articles)
            sources_crawled.append(source)
            logger.info(f"Crawled {len(articles)} articles from {source}")
            
        except Exception as e:
            logger.error(f"Error crawling {source}: {e}")
    
    # Sort by score and limit
    all_articles.sort(key=lambda x: x.get("score", 0), reverse=True)
    all_articles = all_articles[:max_articles]
    
    result = {
        "articles": all_articles,
        "crawl_metadata": {
            "total_fetched": len(all_articles),
            "sources_crawled": sources_crawled,
            "crawl_time": datetime.now(timezone.utc).isoformat(),
        }
    }
    
    # Save to file if output_dir specified
    if output_dir:
        import os
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "crawled_news.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        logger.info(f"Saved results to {output_path}")
    
    return result
