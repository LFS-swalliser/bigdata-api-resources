#!/usr/bin/env python3
"""
News Search Tests for Bigdata Search Tools

Tests 8 key news search scenarios:
1. Entity ID + Date Range
2. Entity ID + Recent Period (last 7 days)
3. Entity ID + Similarity (Tesla Inc + what was reported about earnings)
4. Entity ID + Similarity + Date Range (Tesla Inc + what was reported about earnings + last 30 days)
5. Entity ID + Similarity + Source Filter (Tesla Inc + what was reported about earnings + premium sources)
6. Similarity Only (What did media report about Tesla's stock performance)
7. Similarity Only + Date Range (What did media report about Tesla's stock performance + last 30 days)
8. Breaking News Search (Tesla + today)
"""

import asyncio
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_config import TestConfig, TEST_QUERIES
from bigdata_search_agent.tools import bigdata_news_search

# Rich imports for better table formatting
try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Rich not available. Install with: pip install rich")

class NewsSearchTester:
    """Test suite for news search functionality."""
    
    def __init__(self):
        self.config = TestConfig()
        self.results = []
        self.console = Console() if RICH_AVAILABLE else None
        
        # Test data
        self.test_entity_id = self.config.TEST_ENTITY_ID  # Tesla: DD3BB1
    
    def _extract_first_title(self, result_text: str) -> str:
        """Extract the first title from search results."""
        if "Title:" in result_text:
            lines = result_text.split("\n")
            for line in lines:
                if line.strip().startswith("Title:"):
                    title = line.replace("Title:", "").strip()
                    return title[:60] + "..." if len(title) > 60 else title
        return "No title found"
    
    def _extract_first_content(self, result_text: str) -> str:
        """Extract the first content snippet from search results."""
        if "Content:" in result_text:
            lines = result_text.split("\n")
            for line in lines:
                if line.strip().startswith("Content:"):
                    content = line.replace("Content:", "").strip()
                    return content[:800] + "..." if len(content) > 800 else content
        return "No content found"
    
    async def test_1_entity_id_plus_date_range(self):
        """Test 1: Entity ID + Date Range"""
        print("\n📅 Test 1: Entity ID + Date Range")
        print("-" * 50)
        
        # Single test with one date range - no query needed, just entity and date filtering
        date_range = "last_90_days"
        
        try:
            print(f"\n🔍 Searching Tesla news for date range: {date_range}")
            result = await bigdata_news_search.ainvoke({
                "queries": [""],  # Empty query - pure entity + date filtering
                "max_results": 5,
                "entity_ids": [self.test_entity_id],
                "date_range": date_range
            })
            
            # Extract key info for table display
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} results for {date_range}")
                self.results.append(("entity_date", f"entity:{self.test_entity_id} + date:{date_range}", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No results found for {date_range}")
                self.results.append(("entity_date", f"entity:{self.test_entity_id} + date:{date_range}", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error with date range {date_range}: {str(e)}")
            self.results.append(("entity_date", f"entity:{self.test_entity_id} + date:{date_range}", "error", 0, "N/A", str(e)[:100]))
    
    async def test_2_entity_id_plus_recent_period(self):
        """Test 2: Entity ID + Recent Period (last 7 days)"""
        print("\n⏰ Test 2: Entity ID + Recent Period (last 7 days)")
        print("-" * 50)
        
        # Single test with recent period - no query needed, just entity and recent date filtering
        date_range = "last_7_days"
        
        try:
            print(f"\n🔍 Searching Tesla news for {date_range}")
            result = await bigdata_news_search.ainvoke({
                "queries": [""],  # Empty query - pure entity + date filtering
                "max_results": 5,
                "entity_ids": [self.test_entity_id],
                "date_range": date_range
            })
            
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} results for {date_range}")
                self.results.append(("entity_recent", f"entity:{self.test_entity_id} + {date_range}", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No results found for {date_range}")
                self.results.append(("entity_recent", f"entity:{self.test_entity_id} + {date_range}", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error with recent period {date_range}: {str(e)}")
            self.results.append(("entity_recent", f"entity:{self.test_entity_id} + {date_range}", "error", 0, "N/A", str(e)[:100]))
    
    async def test_3_entity_id_plus_similarity(self):
        """Test 3: Entity ID + Similarity (Tesla Inc + what was reported about earnings)"""
        print("\n🎯 Test 3: Entity ID + Similarity (Tesla Inc + what was reported about earnings)")
        print("-" * 50)
        
        # Single test with one query
        query = "what was reported about earnings"
        
        try:
            print(f"\n🔍 Searching Tesla news for: '{query}'")
            result = await bigdata_news_search.ainvoke({
                "queries": [query],
                "max_results": 5,
                "entity_ids": [self.test_entity_id]
            })
            
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} results for '{query}'")
                self.results.append(("entity_similarity", f"'{query}' + entity:{self.test_entity_id}", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No results found for '{query}'")
                self.results.append(("entity_similarity", f"'{query}' + entity:{self.test_entity_id}", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error searching for '{query}': {str(e)}")
            self.results.append(("entity_similarity", f"'{query}' + entity:{self.test_entity_id}", "error", 0, "N/A", str(e)[:100]))
    
    async def test_4_entity_id_plus_similarity_plus_date_range(self):
        """Test 4: Entity ID + Similarity + Date Range (Tesla Inc + what was reported about earnings + last 30 days)"""
        print("\n📈 Test 4: Entity ID + Similarity + Date Range (Tesla Inc + what was reported about earnings + last 30 days)")
        print("-" * 50)
        
        # Single test with one query
        query = "what was reported about earnings"
        date_range = "last_30_days"
        
        try:
            print(f"\n🔍 Searching Tesla news for: '{query}' in {date_range}")
            result = await bigdata_news_search.ainvoke({
                "queries": [query],
                "max_results": 5,
                "entity_ids": [self.test_entity_id],
                "date_range": date_range
            })
            
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} results for '{query}' in {date_range}")
                self.results.append(("entity_similarity_date", f"'{query}' + entity:{self.test_entity_id} + {date_range}", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No results found for '{query}' in {date_range}")
                self.results.append(("entity_similarity_date", f"'{query}' + entity:{self.test_entity_id} + {date_range}", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error searching for '{query}' in {date_range}: {str(e)}")
            self.results.append(("entity_similarity_date", f"'{query}' + entity:{self.test_entity_id} + {date_range}", "error", 0, "N/A", str(e)[:100]))
    
    async def test_5_entity_id_plus_similarity_plus_rerank(self):
        """Test 5: Entity ID + Similarity + High Rerank Threshold (Tesla Inc + what was reported about earnings + high quality)"""
        print("\n⭐ Test 5: Entity ID + Similarity + High Rerank Threshold (Tesla Inc + what was reported about earnings + high quality)")
        print("-" * 50)
        
        # Single test with one query and high rerank threshold
        query = "what was reported about earnings"
        rerank_threshold = 0.3  # Higher threshold for quality
        
        try:
            print(f"\n🔍 Searching Tesla news for: '{query}' with high quality threshold")
            result = await bigdata_news_search.ainvoke({
                "queries": [query],
                "max_results": 5,
                "entity_ids": [self.test_entity_id],
                "rerank_threshold": rerank_threshold
            })
            
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} high-quality results for '{query}'")
                self.results.append(("entity_similarity_quality", f"'{query}' + entity:{self.test_entity_id} + rerank:0.3", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No high-quality results found for '{query}'")
                self.results.append(("entity_similarity_quality", f"'{query}' + entity:{self.test_entity_id} + rerank:0.3", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error searching with high quality threshold for '{query}': {str(e)}")
            self.results.append(("entity_similarity_quality", f"'{query}' + entity:{self.test_entity_id} + rerank:0.3", "error", 0, "N/A", str(e)[:100]))
    
    async def test_6_similarity_only(self):
        """Test 6: Similarity Only (What did media report about Tesla's stock performance)"""
        print("\n🔍 Test 6: Similarity Only (What did media report about Tesla's stock performance)")
        print("-" * 50)
        
        # Single test with one query
        query = "What did media report about Tesla's stock performance"
        
        try:
            print(f"\n🔍 Open search for: '{query}'")
            result = await bigdata_news_search.ainvoke({
                "queries": [query],
                "max_results": 5
                # No entity_ids - let the query find Tesla mentions naturally
            })
            
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} open search results for '{query}'")
                self.results.append(("similarity_only", f"'{query}' (no entity filter)", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No open search results found for '{query}'")
                self.results.append(("similarity_only", f"'{query}' (no entity filter)", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error with open search for '{query}': {str(e)}")
            self.results.append(("similarity_only", f"'{query}' (no entity filter)", "error", 0, "N/A", str(e)[:100]))
    
    async def test_7_similarity_only_plus_date_range(self):
        """Test 7: Similarity Only + Date Range (What did media report about Tesla's stock performance + last 30 days)"""
        print("\n📅 Test 7: Similarity Only + Date Range (What did media report about Tesla's stock performance + last 30 days)")
        print("-" * 50)
        
        # Single test with one query and one date range
        query = "What did media report about Tesla's stock performance"
        date_range = "last_30_days"
        
        try:
            print(f"\n🔍 Open search for: '{query}' in {date_range}")
            result = await bigdata_news_search.ainvoke({
                "queries": [query],
                "max_results": 5,
                "date_range": date_range
                # No entity_ids - let the query find Tesla mentions naturally
            })
            
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} open search results for '{query}' in {date_range}")
                self.results.append(("similarity_only_date", f"'{query}' + {date_range}", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No open search results found for '{query}' in {date_range}")
                self.results.append(("similarity_only_date", f"'{query}' + {date_range}", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error with open search for '{query}' in {date_range}: {str(e)}")
            self.results.append(("similarity_only_date", f"'{query}' + {date_range}", "error", 0, "N/A", str(e)[:100]))
    
    async def test_8_breaking_news_search(self):
        """Test 8: Breaking News Search (Tesla + today)"""
        print("\n🚨 Test 8: Breaking News Search (Tesla + today)")
        print("-" * 50)
        
        # Single test for breaking news
        query = "Tesla"
        date_range = "today"
        
        try:
            print(f"\n🔍 Breaking news search for: '{query}' {date_range}")
            result = await bigdata_news_search.ainvoke({
                "queries": [query],
                "max_results": 5,
                "entity_ids": [self.test_entity_id],
                "date_range": date_range
            })
            
            result_count = result.count("--- SOURCE") if "--- SOURCE" in result else 0
            first_title = self._extract_first_title(result)
            first_content = self._extract_first_content(result)
            
            if result_count > 0:
                print(f"✅ Found {result_count} breaking news results for '{query}' {date_range}")
                self.results.append(("breaking_news", f"'{query}' + entity:{self.test_entity_id} + {date_range}", "success", result_count, first_title, first_content))
            else:
                print(f"❌ No breaking news found for '{query}' {date_range}")
                self.results.append(("breaking_news", f"'{query}' + entity:{self.test_entity_id} + {date_range}", "error", 0, "N/A", "No results found"))
            
        except Exception as e:
            print(f"❌ Error with breaking news search for '{query}': {str(e)}")
            self.results.append(("breaking_news", f"'{query}' + entity:{self.test_entity_id} + {date_range}", "error", 0, "N/A", str(e)[:100]))
    
    def print_summary(self):
        """Print test summary with Rich tables."""
        print("\n" + "="*60)
        print("🧪 NEWS SEARCH TEST SUMMARY")
        print("="*60)
        
        if RICH_AVAILABLE and self.console:
            # Create detailed results with a better format
            print("\n")
            self.console.print("📊 Detailed Test Results", style="bold blue")
            print()
            
            for i, (test_type, query_info, status, result_count, first_title, first_content) in enumerate(self.results, 1):
                # Create individual panels for each test result
                status_emoji = "✅" if status == "success" else "❌"
                status_color = "green" if status == "success" else "red"
                
                # Create a panel for each test
                self.console.print(f"[bold cyan]Test {i}: {test_type.replace('_', ' ').title()}[/bold cyan]")
                self.console.print(f"[yellow]Query:[/yellow] {query_info}")
                self.console.print(f"[{status_color}]Status:[/{status_color}] {status_emoji} {status.upper()}")
                self.console.print(f"[green]Results Found:[/green] {result_count}")
                
                if first_title and first_title != "No title found":
                    self.console.print(f"[blue]First Title:[/blue] {first_title}")
                
                if first_content and first_content != "No content found":
                    # Show more content without truncation
                    self.console.print(f"[white]First Content:[/white]")
                    self.console.print(f"[dim]{first_content}[/dim]")
                
                # Add separator between tests
                if i < len(self.results):
                    self.console.print("─" * 80, style="dim")
                    print()
            
            # Summary table - much simpler
            print()
            self.console.print("📈 Summary by Test Type", style="bold blue")
            
            summary_table = Table(
                box=box.SIMPLE,
                show_header=True,
                header_style="bold magenta"
            )
            
            summary_table.add_column("Test Type", style="cyan", no_wrap=True)
            summary_table.add_column("Status", justify="center")
            summary_table.add_column("Results", justify="center", style="green")
            summary_table.add_column("Query", style="yellow")
            
            # Group results by test type for summary
            for test_type, query_info, status, result_count, first_title, first_content in self.results:
                status_display = "✅ SUCCESS" if status == "success" else "❌ ERROR"
                query_short = query_info[:50] + "..." if len(query_info) > 50 else query_info
                
                summary_table.add_row(
                    test_type.replace("_", " "),
                    status_display,
                    str(result_count),
                    query_short
                )
            
            self.console.print(summary_table)
            
            # Overall results
            total_tests = len(self.results)
            total_success = sum(1 for _, _, status, _, _, _ in self.results if status == "success")
            overall_success_rate = total_success / total_tests * 100
            
            print("\n")
            self.console.print("🎯 Overall Results", style="bold blue")
            self.console.print(f"• Total tests: [bold]{total_tests}[/bold]")
            self.console.print(f"• Overall success rate: [bold green]{overall_success_rate:.1f}%[/bold green]")
            self.console.print(f"• Test Entity: [bold]{self.config.TEST_COMPANY_NAME}[/bold] ([cyan]{self.test_entity_id}[/cyan])")
            self.console.print(f"• Focus: [italic]8 comprehensive news search test scenarios[/italic]")
            self.console.print(f"• Sources: [bold yellow]Premium news publishers[/bold yellow] (global multilingual)")
            
        else:
            # Fallback to simple text output if Rich not available
            print("\n## 📊 Detailed Test Results (Rich not available - install with: pip install rich)\n")
            
            print("| Test Type | Actual Query + Filters | Status | Results | First Title | First Content |")
            print("|-----------|------------------------|---------|---------|-------------|---------------|")
            
            for test_type, query_info, status, result_count, first_title, first_content in self.results:
                # Truncate long content for table display
                query_display = query_info[:25] + "..." if len(query_info) > 25 else query_info
                title_display = first_title[:40] + "..." if len(first_title) > 40 else first_title
                content_display = first_content[:50] + "..." if len(first_content) > 50 else first_content
                
                # Status emoji
                status_emoji = "✅" if status == "success" else "❌"
                
                print(f"| {test_type} | {query_display} | {status_emoji} {status} | {result_count} | {title_display} | {content_display} |")

async def main():
    """Run all news search tests."""
    print("🧪 Bigdata News Search Tests - 8 Scenarios")
    print("=" * 60)
    
    # Check configuration
    config = TestConfig()
    config.print_config()
    
    if not config.validate_credentials():
        print("\n❌ Cannot run tests without valid credentials")
        return
    
    # Initialize tester
    tester = NewsSearchTester()
    
    # Run all 8 tests
    try:
        await tester.test_1_entity_id_plus_date_range()
        await tester.test_2_entity_id_plus_recent_period()
        await tester.test_3_entity_id_plus_similarity()
        await tester.test_4_entity_id_plus_similarity_plus_date_range()
        await tester.test_5_entity_id_plus_similarity_plus_rerank()
        await tester.test_6_similarity_only()
        await tester.test_7_similarity_only_plus_date_range()
        await tester.test_8_breaking_news_search()
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {str(e)}")
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main()) 