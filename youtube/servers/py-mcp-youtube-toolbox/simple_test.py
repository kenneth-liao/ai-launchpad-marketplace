#!/usr/bin/env python3
"""
Simple test to verify the YouTube MCP server works
"""
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_basic_functionality():
    """Test basic server functionality"""
    print("🧪 Testing YouTube Toolbox MCP Server\n")
    
    try:
        # Import the server module
        from server import search_videos, get_video_details, get_trending_videos
        
        print("✓ Server module imported successfully\n")
        
        # Test 1: Search for videos
        print("Test 1: Searching for videos about 'Python'...")
        search_result = await search_videos(query="Python", max_results=3)
        
        if 'error' in search_result:
            print(f"✗ Search failed: {search_result['error']}")
            return False
        
        if 'items' in search_result and len(search_result['items']) > 0:
            print(f"✓ Found {len(search_result['items'])} videos")
            for i, video in enumerate(search_result['items'][:2], 1):
                print(f"  {i}. {video.get('title', 'N/A')}")
        else:
            print("✗ No videos found")
            return False
        
        print()
        
        # Test 2: Get video details
        print("Test 2: Getting details for a specific video...")
        video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
        video_result = await get_video_details(video_id=video_id)
        
        if 'error' in video_result:
            print(f"✗ Get video details failed: {video_result['error']}")
            return False
        
        if 'title' in video_result:
            print(f"✓ Video: {video_result['title']}")
            print(f"  Channel: {video_result.get('channelTitle', 'N/A')}")
            print(f"  Views: {video_result.get('viewCount', 'N/A')}")
        else:
            print("✗ Video details incomplete")
            return False
        
        print()
        
        # Test 3: Get trending videos
        print("Test 3: Getting trending videos...")
        trending_result = await get_trending_videos(region_code="US", max_results=3)
        
        if 'error' in trending_result:
            print(f"✗ Get trending videos failed: {trending_result['error']}")
            return False
        
        if 'items' in trending_result and len(trending_result['items']) > 0:
            print(f"✓ Found {len(trending_result['items'])} trending videos")
            for i, video in enumerate(trending_result['items'][:2], 1):
                print(f"  {i}. {video.get('title', 'N/A')}")
        else:
            print("✗ No trending videos found")
            return False
        
        print()
        print("=" * 50)
        print("🎉 All tests passed!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main entry point"""
    success = await test_basic_functionality()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())

