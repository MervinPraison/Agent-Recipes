"""
TDD Unit Tests for AI Skill Generator Recipe.

Tests for tools.py functions:
- identify_sources: Find 8 URLs (2 per source type)
- scrape_source: Extract content with type-specific prompts
- format_skill_md: Format content as SKILL.md
- get_extraction_prompt: Get prompt for source type
"""

from unittest.mock import patch


class TestIdentifySources:
    """Tests for identify_sources tool."""
    
    def test_returns_list_of_8_sources(self):
        """identify_sources should return exactly 8 sources."""
        from agent_recipes.templates import skill_generator_tools
        
        # Mock the search and LLM calls
        with patch.object(skill_generator_tools, '_search_for_topic') as mock_search:
            with patch.object(skill_generator_tools, '_categorize_urls') as mock_categorize:
                mock_search.return_value = [
                    {"url": f"https://example{i}.com", "title": f"Title {i}", "snippet": f"Snippet {i}"}
                    for i in range(20)
                ]
                mock_categorize.return_value = [
                    {"url": "https://docs.example.com/react", "type": "docs", "title": "React Docs", "reason": "Official documentation"},
                    {"url": "https://docs.example.com/hooks", "type": "docs", "title": "Hooks Guide", "reason": "Official hooks guide"},
                    {"url": "https://github.com/facebook/react", "type": "github", "title": "React Repo", "reason": "Source code"},
                    {"url": "https://github.com/example/hooks", "type": "github", "title": "Hooks Examples", "reason": "Code examples"},
                    {"url": "https://stackoverflow.com/q/123", "type": "stackoverflow", "title": "React Hooks Q", "reason": "Common question"},
                    {"url": "https://stackoverflow.com/q/456", "type": "stackoverflow", "title": "useEffect Q", "reason": "Best practices"},
                    {"url": "https://blog.example.com/react", "type": "blog", "title": "React Blog", "reason": "Tutorial"},
                    {"url": "https://medium.com/react-hooks", "type": "blog", "title": "Hooks Deep Dive", "reason": "In-depth article"},
                ]
                
                result = skill_generator_tools.identify_sources("react hooks")
                
                assert isinstance(result, list)
                assert len(result) == 8
    
    def test_returns_2_per_source_type(self):
        """identify_sources should return 2 sources per type."""
        from agent_recipes.templates import skill_generator_tools
        
        with patch.object(skill_generator_tools, '_search_for_topic') as mock_search:
            with patch.object(skill_generator_tools, '_categorize_urls') as mock_categorize:
                mock_search.return_value = [{"url": f"https://example{i}.com", "title": f"Title {i}", "snippet": f"Snippet {i}"} for i in range(20)]
                mock_categorize.return_value = [
                    {"url": "https://docs1.com", "type": "docs", "title": "Doc 1", "reason": "R1"},
                    {"url": "https://docs2.com", "type": "docs", "title": "Doc 2", "reason": "R2"},
                    {"url": "https://github1.com", "type": "github", "title": "GH 1", "reason": "R3"},
                    {"url": "https://github2.com", "type": "github", "title": "GH 2", "reason": "R4"},
                    {"url": "https://so1.com", "type": "stackoverflow", "title": "SO 1", "reason": "R5"},
                    {"url": "https://so2.com", "type": "stackoverflow", "title": "SO 2", "reason": "R6"},
                    {"url": "https://blog1.com", "type": "blog", "title": "Blog 1", "reason": "R7"},
                    {"url": "https://blog2.com", "type": "blog", "title": "Blog 2", "reason": "R8"},
                ]
                
                result = skill_generator_tools.identify_sources("react hooks")
                
                type_counts = {}
                for source in result:
                    t = source["type"]
                    type_counts[t] = type_counts.get(t, 0) + 1
                
                assert type_counts.get("docs", 0) == 2
                assert type_counts.get("github", 0) == 2
                assert type_counts.get("stackoverflow", 0) == 2
                assert type_counts.get("blog", 0) == 2
    
    def test_each_source_has_required_fields(self):
        """Each source should have url, type, title, reason."""
        from agent_recipes.templates import skill_generator_tools
        
        with patch.object(skill_generator_tools, '_search_for_topic') as mock_search:
            with patch.object(skill_generator_tools, '_categorize_urls') as mock_categorize:
                mock_search.return_value = [{"url": f"https://example{i}.com", "title": f"Title {i}", "snippet": f"Snippet {i}"} for i in range(20)]
                mock_categorize.return_value = [
                    {"url": "https://docs.example.com", "type": "docs", "title": "React Docs", "reason": "Official"},
                ] * 8
                
                result = skill_generator_tools.identify_sources("react hooks")
                
                for source in result:
                    assert "url" in source
                    assert "type" in source
                    assert "title" in source
                    assert "reason" in source
                    assert source["type"] in ["docs", "github", "stackoverflow", "blog"]


class TestGetExtractionPrompt:
    """Tests for get_extraction_prompt function."""
    
    def test_docs_prompt_focuses_on_api_reference(self):
        """Docs prompt should focus on API reference and examples."""
        from agent_recipes.templates import skill_generator_tools
        
        prompt = skill_generator_tools.get_extraction_prompt("docs")
        
        assert "API" in prompt or "api" in prompt.lower()
        assert "example" in prompt.lower() or "usage" in prompt.lower()
    
    def test_github_prompt_focuses_on_code(self):
        """GitHub prompt should focus on code patterns and implementation."""
        from agent_recipes.templates import skill_generator_tools
        
        prompt = skill_generator_tools.get_extraction_prompt("github")
        
        assert "code" in prompt.lower() or "implementation" in prompt.lower()
    
    def test_stackoverflow_prompt_focuses_on_solutions(self):
        """StackOverflow prompt should focus on problems and solutions."""
        from agent_recipes.templates import skill_generator_tools
        
        prompt = skill_generator_tools.get_extraction_prompt("stackoverflow")
        
        assert "solution" in prompt.lower() or "answer" in prompt.lower() or "problem" in prompt.lower()
    
    def test_blog_prompt_focuses_on_tutorials(self):
        """Blog prompt should focus on tutorials and explanations."""
        from agent_recipes.templates import skill_generator_tools
        
        prompt = skill_generator_tools.get_extraction_prompt("blog")
        
        assert "tutorial" in prompt.lower() or "explanation" in prompt.lower() or "guide" in prompt.lower()
    
    def test_unknown_type_returns_generic_prompt(self):
        """Unknown type should return a generic extraction prompt."""
        from agent_recipes.templates import skill_generator_tools
        
        prompt = skill_generator_tools.get_extraction_prompt("unknown")
        
        assert prompt is not None
        assert len(prompt) > 0


class TestScrapeSource:
    """Tests for scrape_source tool."""
    
    def test_returns_dict_with_content(self):
        """scrape_source should return dict with url, content, extracted."""
        from agent_recipes.templates import skill_generator_tools
        
        with patch.object(skill_generator_tools, '_fetch_url_content') as mock_fetch:
            mock_fetch.return_value = {
                "url": "https://example.com",
                "content": "Full page content here...",
                "success": True
            }
            
            result = skill_generator_tools.scrape_source("https://example.com", "docs")
            
            assert isinstance(result, dict)
            assert "url" in result
            assert "content" in result or "extracted" in result
    
    def test_uses_type_specific_extraction(self):
        """scrape_source should use type-specific extraction prompt."""
        from agent_recipes.templates import skill_generator_tools
        
        with patch.object(skill_generator_tools, '_fetch_url_content') as mock_fetch:
            with patch.object(skill_generator_tools, 'get_extraction_prompt') as mock_prompt:
                mock_fetch.return_value = {"url": "https://example.com", "content": "Content", "success": True}
                mock_prompt.return_value = "Extract API docs..."
                
                skill_generator_tools.scrape_source("https://example.com", "docs")
                
                mock_prompt.assert_called_once_with("docs")
    
    def test_handles_fetch_failure_gracefully(self):
        """scrape_source should handle fetch failures gracefully."""
        from agent_recipes.templates import skill_generator_tools
        
        with patch.object(skill_generator_tools, '_fetch_url_content') as mock_fetch:
            mock_fetch.return_value = {"url": "https://example.com", "content": "", "success": False, "error": "Timeout"}
            
            result = skill_generator_tools.scrape_source("https://example.com", "docs")
            
            assert isinstance(result, dict)
            assert not result.get("success") or result.get("error") is not None


class TestFormatSkillMd:
    """Tests for format_skill_md function."""
    
    def test_includes_quick_start_section(self):
        """SKILL.md should include Quick Start section."""
        from agent_recipes.templates import skill_generator_tools
        
        content = {
            "topic": "React Hooks",
            "sections": {
                "quick_start": "Install with npm install react",
                "core_concepts": "Hooks are functions...",
                "patterns": "useEffect pattern...",
                "pitfalls": "Don't call hooks conditionally"
            }
        }
        
        result = skill_generator_tools.format_skill_md(content)
        
        assert "Quick Start" in result or "quick start" in result.lower()
    
    def test_includes_core_concepts_section(self):
        """SKILL.md should include Core Concepts section."""
        from agent_recipes.templates import skill_generator_tools
        
        content = {
            "topic": "React Hooks",
            "sections": {
                "quick_start": "Install...",
                "core_concepts": "Hooks are functions that let you use state...",
                "patterns": "Pattern...",
                "pitfalls": "Pitfall..."
            }
        }
        
        result = skill_generator_tools.format_skill_md(content)
        
        assert "Core Concepts" in result or "core concepts" in result.lower()
    
    def test_includes_patterns_section(self):
        """SKILL.md should include Essential Patterns section."""
        from agent_recipes.templates import skill_generator_tools
        
        content = {
            "topic": "React Hooks",
            "sections": {
                "quick_start": "Install...",
                "core_concepts": "Concepts...",
                "patterns": "useEffect for side effects, useState for state...",
                "pitfalls": "Pitfall..."
            }
        }
        
        result = skill_generator_tools.format_skill_md(content)
        
        assert "Pattern" in result or "pattern" in result.lower()
    
    def test_includes_pitfalls_section(self):
        """SKILL.md should include Common Pitfalls section."""
        from agent_recipes.templates import skill_generator_tools
        
        content = {
            "topic": "React Hooks",
            "sections": {
                "quick_start": "Install...",
                "core_concepts": "Concepts...",
                "patterns": "Patterns...",
                "pitfalls": "Don't call hooks inside loops or conditions"
            }
        }
        
        result = skill_generator_tools.format_skill_md(content)
        
        assert "Pitfall" in result or "pitfall" in result.lower()
    
    def test_returns_valid_markdown(self):
        """format_skill_md should return valid markdown string."""
        from agent_recipes.templates import skill_generator_tools
        
        content = {
            "topic": "React Hooks",
            "sections": {
                "quick_start": "npm install react",
                "core_concepts": "Hooks are...",
                "patterns": "useEffect...",
                "pitfalls": "Don't..."
            }
        }
        
        result = skill_generator_tools.format_skill_md(content)
        
        assert isinstance(result, str)
        assert "#" in result  # Has markdown headers


class TestGetAllTools:
    """Tests for get_all_tools function."""
    
    def test_returns_list_of_callables(self):
        """get_all_tools should return list of callable functions."""
        from agent_recipes.templates import skill_generator_tools
        
        tools = skill_generator_tools.get_all_tools()
        
        assert isinstance(tools, list)
        assert len(tools) > 0
        for tool in tools:
            assert callable(tool)
    
    def test_includes_identify_sources(self):
        """get_all_tools should include identify_sources."""
        from agent_recipes.templates import skill_generator_tools
        
        tools = skill_generator_tools.get_all_tools()
        tool_names = [t.__name__ for t in tools]
        
        assert "identify_sources" in tool_names
    
    def test_includes_scrape_source(self):
        """get_all_tools should include scrape_source."""
        from agent_recipes.templates import skill_generator_tools
        
        tools = skill_generator_tools.get_all_tools()
        tool_names = [t.__name__ for t in tools]
        
        assert "scrape_source" in tool_names


class TestSourceTypes:
    """Tests for SOURCE_TYPES constant."""
    
    def test_has_four_source_types(self):
        """SOURCE_TYPES should have exactly 4 types."""
        from agent_recipes.templates import skill_generator_tools
        
        assert len(skill_generator_tools.SOURCE_TYPES) == 4
    
    def test_includes_required_types(self):
        """SOURCE_TYPES should include docs, github, stackoverflow, blog."""
        from agent_recipes.templates import skill_generator_tools
        
        assert "docs" in skill_generator_tools.SOURCE_TYPES
        assert "github" in skill_generator_tools.SOURCE_TYPES
        assert "stackoverflow" in skill_generator_tools.SOURCE_TYPES
        assert "blog" in skill_generator_tools.SOURCE_TYPES
