#!/bin/bash
# Recipe Execution Test Script
# Runs all 131 recipes with appropriate test inputs

cd /Users/praison/Agent-Recipes/agent_recipes

LOG_FILE="execution_results.log"
echo "Recipe Execution Tests - $(date)" > "$LOG_FILE"
echo "===============================" >> "$LOG_FILE"

passed=0
failed=0

run_recipe() {
    recipe=$1
    shift
    echo "Testing: $recipe"
    result=$(praisonai recipe run "$recipe" "$@" 2>&1)
    exit_code=$?
    if [ $exit_code -eq 0 ] && echo "$result" | grep -q "completed successfully"; then
        echo "✅ $recipe - PASSED" >> "$LOG_FILE"
        ((passed++))
    else
        echo "❌ $recipe - FAILED" >> "$LOG_FILE"
        echo "Error: $result" >> "$LOG_FILE"
        ((failed++))
    fi
}

# Text/Content recipes
run_recipe ai-ab-hook-tester --var variations="Hook 1: Did you know? | Hook 2: What if I told you?"
run_recipe ai-angle-generator --var topic="renewable energy"
run_recipe ai-blog-generator --var topic="Python programming basics"
run_recipe ai-brief-generator --var project_info="New mobile app for fitness tracking"
run_recipe ai-broll-builder --var script="Introduction to cooking healthy meals"
run_recipe ai-calendar-scheduler --var events="Meeting at 9am, Lunch at 12pm" --var constraints="No meetings after 5pm"
run_recipe ai-chart-generator --var data="Sales: Q1=100, Q2=150, Q3=200" --var chart_type="bar"
run_recipe ai-code-documenter --var code_path="./README.md"
run_recipe ai-code-refactorer --var code_path="./README.md"
run_recipe ai-code-reviewer --var code_path="./README.md"
run_recipe ai-color-palette-extractor --var image_path="./README.md"
run_recipe ai-comment-miner --var url="https://example.com"
run_recipe ai-commit-message-generator --var diff="Added new function to handle user input"
run_recipe ai-content-calendar --var niche="tech" --var duration="1 week"
run_recipe ai-context-enricher --var content="AI is changing the world"
run_recipe ai-cta-generator --var context="Software product landing page" --var goal="increase signups"
run_recipe ai-daily-news-show --var topics="technology, science"
run_recipe ai-email-parser --var email="Subject: Meeting Tomorrow\nFrom: john@test.com\nBody: Let's meet at 3pm."
run_recipe ai-excel-formula-generator --var description="Sum values if condition met" --var context="Sales spreadsheet"
run_recipe ai-fact-checker --var claims="The Earth is round"
run_recipe ai-faq-generator --var topic="online shopping" --var context="E-commerce FAQ"
run_recipe ai-hashtag-optimizer --var content="New product launch" --var platform="Instagram"
run_recipe ai-hook-generator --var topic="productivity tips" --var platform="TikTok"
run_recipe ai-log-analyzer --var log_content="ERROR: Connection failed at 12:00\nWARN: Slow response at 12:05"
run_recipe ai-meeting-summarizer --var transcript="John: Let's discuss the project. Mary: I agree we need more time."
run_recipe ai-meta-tag-generator --var url="https://example.com"
run_recipe ai-news-crawler --var topic="artificial intelligence"
run_recipe ai-news-deduper --var articles="Article 1: AI breakthrough | Article 2: AI breakthrough announced"
run_recipe ai-newsletter-generator --var topic="weekly tech news"
run_recipe ai-note-summarizer --var notes="Meeting notes: discussed budget, timeline, resources needed."
run_recipe ai-performance-analyzer --var metrics="Views: 1000, Clicks: 50, Conversions: 5"
run_recipe ai-post-copy-generator --var content="New product launch" --var platform="LinkedIn"
run_recipe ai-product-description-generator --var product_name="Wireless Earbuds" --var features="Bluetooth 5.0, 24hr battery"
run_recipe ai-publisher-pack --var content="Introduction to machine learning"
run_recipe ai-regex-generator --var description="Match phone numbers" --var examples="555-123-4567"
run_recipe ai-report-generator --var data="Sales: 100, Revenue: 5000" --var report_type="monthly"
run_recipe ai-schema-generator --var data_sample='{"name": "John", "age": 30}'
run_recipe ai-script-writer --var topic="how to cook pasta" --var format="YouTube video"
run_recipe ai-sentiment-analyzer --var text="I love this product!"
run_recipe ai-seo-optimizer --var content="Blog about gardening tips" --var keywords="gardening, plants"
run_recipe ai-signal-ranker --var signals="High engagement, trending topic, viral potential"
run_recipe ai-slide-generator --var topic="company overview" --var num_slides="5"
run_recipe ai-slide-to-notes --var slide_path="./README.md"
run_recipe ai-social-media-generator --var topic="product launch" --var platforms="Twitter, LinkedIn"
run_recipe ai-sql-generator --var description="Get all users who signed up last month" --var schema="users(id, name, email, signup_date)"
run_recipe ai-test-generator --var code_path="./README.md"
run_recipe ai-translation-batch --var content="Hello, how are you?" --var target_languages="Spanish, French"
run_recipe ai-contract-analyzer --var contract_path="./README.md"
run_recipe ai-csv-cleaner --var csv_path="./README.md"
run_recipe ai-data-anonymizer --var data_path="./README.md"
run_recipe ai-data-profiler --var data_path="./README.md"
run_recipe ai-doc-translator --var doc_path="./README.md" --var target_language="Spanish"
run_recipe ai-etl-pipeline --var source="MySQL database" --var destination="PostgreSQL"
run_recipe ai-form-filler --var form_fields="name, email, phone" --var data="John Doe, john@test.com, 555-1234"
run_recipe ai-invoice-processor --var invoice_path="./README.md"
run_recipe ai-json-to-csv --var json_path="./README.md"
run_recipe ai-pdf-summarizer --var pdf_path="./README.md"
run_recipe ai-pdf-to-markdown --var pdf_path="./README.md"
run_recipe ai-resume-parser --var resume_path="./README.md"
run_recipe ai-url-to-markdown --var url="https://example.com"
run_recipe ai-dependency-auditor --var project_path="."
run_recipe ai-api-doc-generator --var code_path="./README.md"
run_recipe ai-api-tester --var api_spec="GET /users returns list of users"
run_recipe ai-changelog-generator --var repo_path="."
run_recipe ai-duplicate-finder --var directory_path="."
run_recipe ai-file-organizer --var directory_path="."
run_recipe ai-folder-packager --var folder_path="."
run_recipe ai-repo-readme --var repo_path="."

# Media recipes (may need actual files, using placeholder)
run_recipe ai-audio-enhancer --var audio_path="test.mp3"
run_recipe ai-audio-normalizer --var audio_path="test.mp3"
run_recipe ai-audio-splitter --var audio_path="test.mp3"
run_recipe ai-background-music-generator --var mood="upbeat" --var duration="30"
run_recipe ai-background-remover --var image_path="test.jpg"
run_recipe ai-barcode-scanner --var image_path="test.jpg"
run_recipe ai-ebook-converter --var input_path="test.epub" --var output_format="pdf"
run_recipe ai-face-blur --var image_path="test.jpg"
run_recipe ai-image-captioner --var image_path="test.jpg"
run_recipe ai-image-cataloger --var directory_path="."
run_recipe ai-image-optimizer --var image_path="test.jpg" --var target_size="100KB"
run_recipe ai-image-resizer --var image_path="test.jpg" --var dimensions="800x600"
run_recipe ai-image-tagger --var image_path="test.jpg"
run_recipe ai-image-upscaler --var image_path="test.jpg"
run_recipe ai-markdown-to-pdf --var md_path="./README.md"
run_recipe ai-podcast-cleaner --var audio_path="test.mp3"
run_recipe ai-podcast-transcriber --var audio_path="test.mp3"
run_recipe ai-qr-code-generator --var content="https://example.com"
run_recipe ai-rss-aggregator --var rss_urls="https://example.com/feed"
run_recipe ai-screen-recorder --var duration="10"
run_recipe ai-screenshot-capture --var url="https://example.com"
run_recipe ai-screenshot-ocr --var image_path="test.jpg"
run_recipe ai-sitemap-generator --var url="https://example.com"
run_recipe ai-sitemap-scraper --var sitemap_url="https://example.com/sitemap.xml"
run_recipe ai-subtitle-generator --var video_path="test.mp4"
run_recipe ai-video-chapter-generator --var video_path="test.mp4"
run_recipe ai-video-compressor --var video_path="test.mp4"
run_recipe ai-video-editor --var video_path="test.mp4"
run_recipe ai-video-highlight-extractor --var video_path="test.mp4"
run_recipe ai-video-merger --var video_paths="video1.mp4,video2.mp4"
run_recipe ai-video-thumbnails --var video_path="test.mp4"
run_recipe ai-video-to-gif --var video_path="test.mp4" --var duration="5"
run_recipe ai-voice-cloner --var voice_sample="test.mp3" --var text="Hello world"
run_recipe ai-voiceover-generator --var script="Welcome to the show" --var voice_style="professional"
run_recipe ai-watermark-adder --var image_path="test.jpg" --var watermark_text="Copyright 2026"
run_recipe ai-watermark-remover --var image_path="test.jpg"

# Special/Complex recipes
run_recipe ai-news-capture-pack --var sources="CNN, BBC"
run_recipe ai-product-announcement --var product="New AI Product" --var features="fast, reliable"
run_recipe ai-quick-news --var topic="technology"
run_recipe ai-research-pipeline --var topic="climate change"
run_recipe ai-topic-gatherer --var niche="technology"
run_recipe data-transformer --var input_path="./README.md" --var output_format="json"
run_recipe url-to-blog --var url="https://example.com"

echo "" >> "$LOG_FILE"
echo "===============================" >> "$LOG_FILE"
echo "SUMMARY: Passed=$passed, Failed=$failed" >> "$LOG_FILE"
echo "Test completed at $(date)" >> "$LOG_FILE"

echo "Results saved to $LOG_FILE"
echo "Passed: $passed, Failed: $failed"
