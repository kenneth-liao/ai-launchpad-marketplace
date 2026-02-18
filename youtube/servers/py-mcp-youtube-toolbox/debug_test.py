#!/usr/bin/env python3
"""Debug test to see detailed error messages"""
import asyncio
from dotenv import load_dotenv
import json

load_dotenv()

async def debug_trending():
    from server import get_trending_videos
    
    print("Testing trending videos with detailed output...\n")
    result = await get_trending_videos(region_code="US", max_results=3)
    
    print("Full result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(debug_trending())

