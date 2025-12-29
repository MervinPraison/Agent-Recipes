"""
AI Daily News Show Tools

End-to-end pipeline orchestrator for daily AI news show production.
Coordinates: crawl → rank → select → scripts → capture → voice → video → shorts → bundle
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def run_pipeline(
    date: Optional[str] = None,
    sources: Optional[List[str]] = None,
    max_stories: int = 3,
    human_approval: bool = False,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the complete daily news show pipeline.
    
    Args:
        date: Date for the show (default: today)
        sources: News sources to crawl
        max_stories: Maximum stories to include
        human_approval: Require human approval at key stages
        output_dir: Output directory
        
    Returns:
        Pipeline results with all outputs
    """
    date = date or datetime.now().strftime("%Y-%m-%d")
    sources = sources or ["hackernews", "reddit", "arxiv"]
    output_dir = output_dir or f"./daily_show_{date.replace('-', '')}"
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    pipeline_log = {
        "date": date,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stages": [],
        "status": "running",
    }
    
    try:
        # Stage 1: Crawl
        logger.info("Stage 1: Crawling news sources...")
        from agent_recipes.templates.ai_news_crawler import tools as crawler
        crawl_result = crawler.crawl_ai_news(sources=sources, max_articles=50)
        articles = crawl_result.get("articles", [])
        pipeline_log["stages"].append({"stage": "crawl", "status": "complete", "articles": len(articles)})
        
        # Stage 2: Dedupe
        logger.info("Stage 2: Deduplicating articles...")
        from agent_recipes.templates.ai_news_deduper import tools as deduper
        dedup_result = deduper.deduplicate_articles(articles, use_semantic=False)
        articles = dedup_result.get("deduplicated", articles)
        pipeline_log["stages"].append({"stage": "dedupe", "status": "complete", "remaining": len(articles)})
        
        # Stage 3: Rank
        logger.info("Stage 3: Ranking articles...")
        from agent_recipes.templates.ai_signal_ranker import tools as ranker
        rank_result = ranker.rank_articles(articles, top_n=max_stories * 2)
        articles = rank_result.get("ranked_articles", articles)
        pipeline_log["stages"].append({"stage": "rank", "status": "complete"})
        
        # Stage 4: Select top stories
        logger.info(f"Stage 4: Selecting top {max_stories} stories...")
        selected = articles[:max_stories]
        
        if human_approval:
            # Save for human review
            review_path = os.path.join(output_dir, "stories_for_review.json")
            with open(review_path, "w") as f:
                json.dump(selected, f, indent=2)
            pipeline_log["stages"].append({"stage": "select", "status": "awaiting_approval", "path": review_path})
            pipeline_log["status"] = "awaiting_approval"
            return {"pipeline_log": pipeline_log, "awaiting_approval": True}
        
        pipeline_log["stages"].append({"stage": "select", "status": "complete", "selected": len(selected)})
        
        # Stage 5: Generate scripts
        logger.info("Stage 5: Generating scripts...")
        scripts = []
        from agent_recipes.templates.ai_script_writer import tools as writer
        
        for i, story in enumerate(selected):
            script_result = writer.write_youtube_script(
                topic=story.get("title", "AI News"),
                target_length=180,
                key_points=[story.get("content", "")[:200]],
            )
            scripts.append({
                "story_index": i,
                "title": story.get("title"),
                "script": script_result.get("script", ""),
            })
            
            # Save script
            script_path = os.path.join(output_dir, f"script_{i}.md")
            with open(script_path, "w") as f:
                f.write(f"# {story.get('title')}\n\n{script_result.get('script', '')}")
        
        pipeline_log["stages"].append({"stage": "script", "status": "complete", "scripts": len(scripts)})
        
        # Stage 6: Generate voiceovers
        logger.info("Stage 6: Generating voiceovers...")
        voiceovers = []
        from agent_recipes.templates.ai_voiceover_generator import tools as voice
        
        for i, script in enumerate(scripts):
            vo_result = voice.generate_voiceover(
                text=script.get("script", "")[:4000],
                output_path=os.path.join(output_dir, f"voiceover_{i}.mp3"),
            )
            if "path" in vo_result:
                voiceovers.append(vo_result["path"])
        
        pipeline_log["stages"].append({"stage": "voiceover", "status": "complete", "files": len(voiceovers)})
        
        # Stage 7: Bundle outputs
        logger.info("Stage 7: Creating output bundle...")
        bundle_result = bundle_outputs(
            output_dir=output_dir,
            scripts=scripts,
            voiceovers=voiceovers,
            articles=selected,
        )
        
        pipeline_log["stages"].append({"stage": "bundle", "status": "complete"})
        pipeline_log["status"] = "complete"
        pipeline_log["completed_at"] = datetime.now(timezone.utc).isoformat()
        
        # Save pipeline log
        log_path = os.path.join(output_dir, "pipeline_log.json")
        with open(log_path, "w") as f:
            json.dump(pipeline_log, f, indent=2)
        
        return {
            "status": "complete",
            "output_dir": output_dir,
            "bundle": bundle_result,
            "scripts": scripts,
            "voiceovers": voiceovers,
            "pipeline_log": pipeline_log,
        }
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        pipeline_log["status"] = "failed"
        pipeline_log["error"] = str(e)
        return {"status": "failed", "error": str(e), "pipeline_log": pipeline_log}


def check_stage_status(
    output_dir: str,
    stage: str,
) -> Dict[str, Any]:
    """
    Check the status of a pipeline stage.
    
    Args:
        output_dir: Pipeline output directory
        stage: Stage name to check
        
    Returns:
        Stage status
    """
    log_path = os.path.join(output_dir, "pipeline_log.json")
    
    if not os.path.exists(log_path):
        return {"status": "not_found"}
    
    with open(log_path) as f:
        log = json.load(f)
    
    for s in log.get("stages", []):
        if s.get("stage") == stage:
            return s
    
    return {"status": "not_started"}


def request_approval(
    output_dir: str,
    stage: str,
    items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Request human approval for a stage.
    
    Args:
        output_dir: Pipeline output directory
        stage: Stage requiring approval
        items: Items to approve
        
    Returns:
        Approval request info
    """
    approval_path = os.path.join(output_dir, f"approval_{stage}.json")
    
    approval_request = {
        "stage": stage,
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
        "status": "pending",
    }
    
    with open(approval_path, "w") as f:
        json.dump(approval_request, f, indent=2)
    
    return {
        "approval_path": approval_path,
        "status": "pending",
        "items_count": len(items),
    }


def bundle_outputs(
    output_dir: str,
    scripts: List[Dict[str, Any]],
    voiceovers: List[str],
    articles: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Bundle all pipeline outputs.
    
    Args:
        output_dir: Output directory
        scripts: Generated scripts
        voiceovers: Voiceover file paths
        articles: Source articles
        
    Returns:
        Bundle info
    """
    bundle_manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scripts": [
            {"index": s["story_index"], "title": s["title"]}
            for s in scripts
        ],
        "voiceovers": voiceovers,
        "articles": [
            {"title": a.get("title"), "url": a.get("url"), "source": a.get("source")}
            for a in articles
        ],
    }
    
    manifest_path = os.path.join(output_dir, "bundle_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(bundle_manifest, f, indent=2)
    
    return {
        "manifest_path": manifest_path,
        "output_dir": output_dir,
        "total_scripts": len(scripts),
        "total_voiceovers": len(voiceovers),
    }


def resume_pipeline(
    output_dir: str,
    approved_items: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """
    Resume a pipeline after human approval.
    
    Args:
        output_dir: Pipeline output directory
        approved_items: Indices of approved items
        
    Returns:
        Resumed pipeline results
    """
    log_path = os.path.join(output_dir, "pipeline_log.json")
    
    if not os.path.exists(log_path):
        return {"error": "Pipeline log not found"}
    
    with open(log_path) as f:
        log = json.load(f)
    
    if log.get("status") != "awaiting_approval":
        return {"error": "Pipeline not awaiting approval"}
    
    # Load stories for review
    review_path = os.path.join(output_dir, "stories_for_review.json")
    with open(review_path) as f:
        stories = json.load(f)
    
    # Filter to approved items
    if approved_items:
        stories = [stories[i] for i in approved_items if i < len(stories)]
    
    # Continue pipeline from script generation
    return run_pipeline(
        date=log.get("date"),
        max_stories=len(stories),
        human_approval=False,
        output_dir=output_dir,
    )
