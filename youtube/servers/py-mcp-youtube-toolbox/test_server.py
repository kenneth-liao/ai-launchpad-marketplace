#!/usr/bin/env python3
"""
Comprehensive test script for YouTube Toolbox MCP Server
Tests all tools, resources, and prompts
"""
import asyncio
import json
import os
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

# Test video IDs (public videos that should have transcripts)
TEST_VIDEO_ID = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
TEST_CHANNEL_ID = "UCuAXFkgsw1L7xaCfnd5JJOw"  # Rick Astley's channel

class MCPServerTester:
    """Test harness for MCP server"""
    
    def __init__(self):
        self.results = {
            "passed": [],
            "failed": [],
            "skipped": []
        }
        
    async def test_search_videos(self) -> Dict[str, Any]:
        """Test search_videos tool"""
        console.print("\n[bold cyan]Testing: search_videos[/bold cyan]")
        
        try:
            from server import search_videos
            
            result = await search_videos(
                query="MCP server",
                max_results=5,
                order="relevance"
            )
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'items' in result and len(result['items']) > 0:
                console.print(f"✓ Found {len(result['items'])} videos")
                return {"status": "passed", "data": result}
            else:
                return {"status": "failed", "error": "No videos found"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_get_video_details(self) -> Dict[str, Any]:
        """Test get_video_details tool"""
        console.print("\n[bold cyan]Testing: get_video_details[/bold cyan]")
        
        try:
            from server import get_video_details
            
            result = await get_video_details(video_id=TEST_VIDEO_ID)
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'title' in result and 'channelTitle' in result:
                console.print(f"✓ Video: {result['title']}")
                console.print(f"✓ Channel: {result['channelTitle']}")
                console.print(f"✓ Views: {result.get('viewCount', 'N/A')}")
                return {"status": "passed", "data": result}
            else:
                return {"status": "failed", "error": "Missing video details"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_get_channel_details(self) -> Dict[str, Any]:
        """Test get_channel_details tool"""
        console.print("\n[bold cyan]Testing: get_channel_details[/bold cyan]")
        
        try:
            from server import get_channel_details
            
            result = await get_channel_details(channel_id=TEST_CHANNEL_ID)
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'title' in result:
                console.print(f"✓ Channel: {result['title']}")
                console.print(f"✓ Subscribers: {result.get('subscriberCount', 'N/A')}")
                console.print(f"✓ Videos: {result.get('videoCount', 'N/A')}")
                return {"status": "passed", "data": result}
            else:
                return {"status": "failed", "error": "Missing channel details"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_get_video_comments(self) -> Dict[str, Any]:
        """Test get_video_comments tool"""
        console.print("\n[bold cyan]Testing: get_video_comments[/bold cyan]")
        
        try:
            from server import get_video_comments
            
            result = await get_video_comments(
                video_id=TEST_VIDEO_ID,
                max_results=5,
                order="relevance"
            )
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'comments' in result:
                console.print(f"✓ Found {len(result['comments'])} comments")
                return {"status": "passed", "data": result}
            else:
                return {"status": "failed", "error": "No comments found"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_get_video_transcript(self) -> Dict[str, Any]:
        """Test get_video_transcript tool"""
        console.print("\n[bold cyan]Testing: get_video_transcript[/bold cyan]")
        
        try:
            from server import get_video_transcript
            
            result = await get_video_transcript(
                video_id=TEST_VIDEO_ID,
                language="en"
            )
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'transcript' in result and len(result['transcript']) > 0:
                console.print(f"✓ Found {len(result['transcript'])} transcript segments")
                return {"status": "passed", "data": result}
            else:
                return {"status": "failed", "error": "No transcript found"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_get_related_videos(self) -> Dict[str, Any]:
        """Test get_related_videos tool"""
        console.print("\n[bold cyan]Testing: get_related_videos[/bold cyan]")
        
        try:
            from server import get_related_videos
            
            result = await get_related_videos(
                video_id=TEST_VIDEO_ID,
                max_results=5
            )
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'items' in result and len(result['items']) > 0:
                console.print(f"✓ Found {len(result['items'])} related videos")
                return {"status": "passed", "data": result}
            else:
                return {"status": "failed", "error": "No related videos found"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_get_trending_videos(self) -> Dict[str, Any]:
        """Test get_trending_videos tool"""
        console.print("\n[bold cyan]Testing: get_trending_videos[/bold cyan]")
        
        try:
            from server import get_trending_videos
            
            result = await get_trending_videos(
                region_code="US",
                max_results=5
            )
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'items' in result and len(result['items']) > 0:
                console.print(f"✓ Found {len(result['items'])} trending videos")
                return {"status": "passed", "data": result}
            else:
                return {"status": "failed", "error": "No trending videos found"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_get_video_enhanced_transcript(self) -> Dict[str, Any]:
        """Test get_video_enhanced_transcript tool"""
        console.print("\n[bold cyan]Testing: get_video_enhanced_transcript[/bold cyan]")
        
        try:
            from server import get_video_enhanced_transcript
            
            result = await get_video_enhanced_transcript(
                video_ids=[TEST_VIDEO_ID],
                language="en",
                format="timestamped",
                include_metadata=True
            )
            
            if 'error' in result:
                return {"status": "failed", "error": result['error']}
            
            if 'videos' in result and len(result['videos']) > 0:
                video = result['videos'][0]
                if 'transcript' in video:
                    console.print(f"✓ Enhanced transcript retrieved")
                    console.print(f"✓ Format: timestamped")
                    return {"status": "passed", "data": result}
                else:
                    return {"status": "failed", "error": "No transcript in result"}
            else:
                return {"status": "failed", "error": "No videos in result"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_resources(self) -> Dict[str, Any]:
        """Test MCP resources"""
        console.print("\n[bold cyan]Testing: MCP Resources[/bold cyan]")
        
        try:
            from server import get_available_youtube_tools, get_video_resource
            
            # Test available tools resource
            tools = await get_available_youtube_tools()
            console.print(f"✓ Found {len(tools)} available tools")
            
            # Test video resource
            video_resource = await get_video_resource(video_id=TEST_VIDEO_ID)
            if 'contents' in video_resource:
                console.print(f"✓ Video resource retrieved")
                return {"status": "passed", "data": {"tools": tools, "video": video_resource}}
            else:
                return {"status": "failed", "error": "Video resource missing contents"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def run_all_tests(self):
        """Run all tests and display results"""
        console.print(Panel.fit(
            "[bold green]YouTube Toolbox MCP Server Test Suite[/bold green]",
            border_style="green"
        ))
        
        # Check for API key
        if not os.getenv("YOUTUBE_API_KEY"):
            console.print("[bold red]ERROR: YOUTUBE_API_KEY not found in environment[/bold red]")
            console.print("Please set your YouTube API key in .env file")
            return
        
        tests = [
            ("search_videos", self.test_search_videos),
            ("get_video_details", self.test_get_video_details),
            ("get_channel_details", self.test_get_channel_details),
            ("get_video_comments", self.test_get_video_comments),
            ("get_video_transcript", self.test_get_video_transcript),
            ("get_related_videos", self.test_get_related_videos),
            ("get_trending_videos", self.test_get_trending_videos),
            ("get_video_enhanced_transcript", self.test_get_video_enhanced_transcript),
            ("resources", self.test_resources),
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running tests...", total=len(tests))
            
            for test_name, test_func in tests:
                try:
                    result = await test_func()
                    
                    if result["status"] == "passed":
                        self.results["passed"].append(test_name)
                    elif result["status"] == "failed":
                        self.results["failed"].append({
                            "name": test_name,
                            "error": result.get("error", "Unknown error")
                        })
                    else:
                        self.results["skipped"].append(test_name)
                        
                except Exception as e:
                    self.results["failed"].append({
                        "name": test_name,
                        "error": str(e)
                    })
                
                progress.advance(task)
        
        # Display results
        self.display_results()
    
    def display_results(self):
        """Display test results in a formatted table"""
        console.print("\n")
        
        # Summary table
        table = Table(title="Test Results Summary", show_header=True, header_style="bold magenta")
        table.add_column("Status", style="cyan", width=12)
        table.add_column("Count", justify="right", style="green")
        
        table.add_row("✓ Passed", str(len(self.results["passed"])))
        table.add_row("✗ Failed", str(len(self.results["failed"])))
        table.add_row("⊘ Skipped", str(len(self.results["skipped"])))
        
        console.print(table)
        
        # Failed tests details
        if self.results["failed"]:
            console.print("\n[bold red]Failed Tests:[/bold red]")
            for failed in self.results["failed"]:
                console.print(f"  ✗ {failed['name']}: {failed['error']}")
        
        # Success message
        if len(self.results["failed"]) == 0:
            console.print("\n[bold green]🎉 All tests passed![/bold green]")
        else:
            console.print(f"\n[bold yellow]⚠ {len(self.results['failed'])} test(s) failed[/bold yellow]")

async def main():
    """Main entry point"""
    tester = MCPServerTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

