"""
Integration Tests for AI Skill Generator Recipe.

Tests the full recipe execution flow:
- Recipe YAML parsing
- Tool loading from tools.py
- Step execution with variable substitution
- Output file generation

Run with: pytest tests/integration/test_skill_generator_integration.py -v
"""

import sys
from pathlib import Path
from unittest.mock import patch

# Add templates to path for imports
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "agent_recipes" / "templates"
sys.path.insert(0, str(TEMPLATES_DIR))


class TestRecipeStructure:
    """Tests for recipe file structure and validity."""
    
    def test_recipe_folder_exists(self, templates_dir):
        """Recipe folder should exist with required files."""
        recipe_dir = templates_dir / "ai-skill-generator"
        
        assert recipe_dir.exists(), "ai-skill-generator folder should exist"
        assert (recipe_dir / "agents.yaml").exists(), "agents.yaml should exist"
        assert (recipe_dir / "tools.py").exists(), "tools.py should exist"
    
    def test_agents_yaml_is_valid(self, templates_dir):
        """agents.yaml should be valid YAML."""
        import yaml
        
        recipe_dir = templates_dir / "ai-skill-generator"
        yaml_path = recipe_dir / "agents.yaml"
        
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
        
        assert config is not None
        assert "agents" in config
        assert "steps" in config
    
    def test_agents_yaml_has_required_agents(self, templates_dir):
        """agents.yaml should define source_finder, scraper, synthesizer."""
        import yaml
        
        recipe_dir = templates_dir / "ai-skill-generator"
        yaml_path = recipe_dir / "agents.yaml"
        
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
        
        agents = config.get("agents", {})
        assert "source_finder" in agents
        assert "scraper" in agents
        assert "synthesizer" in agents
    
    def test_agents_have_tool_choice_required(self, templates_dir):
        """Agents with tools should have tool_choice: required."""
        import yaml
        
        recipe_dir = templates_dir / "ai-skill-generator"
        yaml_path = recipe_dir / "agents.yaml"
        
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
        
        agents = config.get("agents", {})
        
        # source_finder has tools, should have tool_choice
        source_finder = agents.get("source_finder", {})
        assert source_finder.get("tools"), "source_finder should have tools"
        assert source_finder.get("tool_choice") == "required"
        
        # scraper has tools, should have tool_choice
        scraper = agents.get("scraper", {})
        assert scraper.get("tools"), "scraper should have tools"
        assert scraper.get("tool_choice") == "required"
    
    def test_steps_include_parallel_loop(self, templates_dir):
        """Steps should include a parallel loop for scraping."""
        import yaml
        
        recipe_dir = templates_dir / "ai-skill-generator"
        yaml_path = recipe_dir / "agents.yaml"
        
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
        
        steps = config.get("steps", [])
        
        # Find the loop step
        loop_step = None
        for step in steps:
            if "loop" in step:
                loop_step = step
                break
        
        assert loop_step is not None, "Should have a loop step"
        assert loop_step["loop"].get("parallel") is True, "Loop should be parallel"
        assert loop_step["loop"].get("max_workers", 0) > 0, "Should have max_workers"


class TestToolsLoading:
    """Tests for tools.py loading and registration."""
    
    def test_tools_module_imports(self, templates_dir):
        """tools.py should import without errors."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            assert tools is not None
        finally:
            sys.path.remove(str(recipe_dir))
    
    def test_get_all_tools_returns_functions(self, templates_dir):
        """get_all_tools should return list of callable functions."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            all_tools = tools.get_all_tools()
            
            assert isinstance(all_tools, list)
            assert len(all_tools) >= 3  # identify_sources, scrape_source, format_skill_md
            
            for tool in all_tools:
                assert callable(tool)
        finally:
            sys.path.remove(str(recipe_dir))
    
    def test_tools_have_docstrings(self, templates_dir):
        """All tools should have docstrings for LLM understanding."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            all_tools = tools.get_all_tools()
            
            for tool in all_tools:
                assert tool.__doc__ is not None, f"{tool.__name__} should have docstring"
                assert len(tool.__doc__) > 20, f"{tool.__name__} docstring too short"
        finally:
            sys.path.remove(str(recipe_dir))


class TestIdentifySourcesIntegration:
    """Integration tests for identify_sources tool."""
    
    def test_identify_sources_with_mock_search(self, templates_dir):
        """identify_sources should work with mocked search."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            # Mock the search function
            mock_results = [
                {"url": "https://react.dev/reference/react/hooks", "title": "React Hooks", "snippet": "Official docs"},
                {"url": "https://react.dev/learn/state-a-components-memory", "title": "State Guide", "snippet": "Learn state"},
                {"url": "https://github.com/facebook/react", "title": "React Repo", "snippet": "Source code"},
                {"url": "https://github.com/streamich/react-use", "title": "react-use", "snippet": "Hook library"},
                {"url": "https://stackoverflow.com/questions/53945763", "title": "useEffect Q", "snippet": "Question"},
                {"url": "https://stackoverflow.com/questions/54069253", "title": "useState Q", "snippet": "Question"},
                {"url": "https://blog.logrocket.com/react-hooks-cheat-sheet", "title": "Hooks Cheat Sheet", "snippet": "Tutorial"},
                {"url": "https://medium.com/react-hooks-guide", "title": "Hooks Guide", "snippet": "Deep dive"},
            ]
            
            with patch.object(tools, '_search_for_topic', return_value=mock_results):
                sources = tools.identify_sources("react hooks")
                
                assert len(sources) == 8
                
                # Check type distribution
                types = [s["type"] for s in sources]
                assert types.count("docs") == 2
                assert types.count("github") == 2
                assert types.count("stackoverflow") == 2
                assert types.count("blog") == 2
        finally:
            sys.path.remove(str(recipe_dir))


class TestScrapeSourceIntegration:
    """Integration tests for scrape_source tool."""
    
    def test_scrape_source_with_mock_crawl(self, templates_dir):
        """scrape_source should work with mocked crawl."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            mock_content = {
                "url": "https://react.dev/reference/react/useState",
                "content": "useState is a React Hook that lets you add state to a function component...",
                "title": "useState – React",
                "success": True
            }
            
            with patch.object(tools, '_fetch_url_content', return_value=mock_content):
                result = tools.scrape_source("https://react.dev/reference/react/useState", "docs")
                
                assert result["success"] is True
                assert "useState" in result["content"]
                assert result["source_type"] == "docs"
        finally:
            sys.path.remove(str(recipe_dir))


class TestFormatSkillMdIntegration:
    """Integration tests for format_skill_md tool."""
    
    def test_format_skill_md_creates_valid_markdown(self, templates_dir):
        """format_skill_md should create valid markdown structure."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            content = {
                "topic": "React Hooks",
                "sections": {
                    "quick_start": "```bash\nnpm install react\n```\n\nThen use hooks in your components.",
                    "core_concepts": "Hooks let you use state and other React features without writing a class.",
                    "patterns": "```jsx\nconst [count, setCount] = useState(0);\n```",
                    "pitfalls": "Don't call hooks inside loops, conditions, or nested functions."
                }
            }
            
            md = tools.format_skill_md(content)
            
            # Check structure
            assert "# React Hooks" in md
            assert "## Quick Start" in md
            assert "## Core Concepts" in md
            assert "## Essential Patterns" in md
            assert "## Common Pitfalls" in md
            assert "## Sources" in md
            
            # Check content
            assert "npm install react" in md
            assert "useState" in md
        finally:
            sys.path.remove(str(recipe_dir))


class TestContextManagement:
    """Tests for context management configuration."""
    
    def test_context_config_exists(self, templates_dir):
        """agents.yaml should have context management config."""
        import yaml
        
        recipe_dir = templates_dir / "ai-skill-generator"
        yaml_path = recipe_dir / "agents.yaml"
        
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
        
        context = config.get("context", {})
        assert context.get("enabled") is True
        assert "max_tool_output_tokens" in context


class TestVariableSubstitution:
    """Tests for variable substitution in recipe."""
    
    def test_topic_variable_in_agents(self, templates_dir):
        """Agents should reference {{topic}} variable."""
        recipe_dir = templates_dir / "ai-skill-generator"
        yaml_path = recipe_dir / "agents.yaml"
        
        with open(yaml_path) as f:
            content = f.read()
        
        # Check that topic variable is used
        assert "{{topic}}" in content
    
    def test_output_file_uses_topic(self, templates_dir):
        """Output file should use topic in filename."""
        import yaml
        
        recipe_dir = templates_dir / "ai-skill-generator"
        yaml_path = recipe_dir / "agents.yaml"
        
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
        
        steps = config.get("steps", [])
        
        # Find the synthesize step
        for step in steps:
            if step.get("name") == "synthesize_skill":
                output_file = step.get("output_file", "")
                assert "{{topic}}" in output_file or "SKILL" in output_file
                break
