#!/bin/bash

# Quick Test Script for YouTube Toolbox MCP Server
# This script helps you quickly test the MCP server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}YouTube Toolbox MCP Server Quick Test${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}✗ .env file not found${NC}"
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp env.example .env
    echo -e "${YELLOW}Please edit .env and add your YouTube API key:${NC}"
    echo -e "${YELLOW}  YOUTUBE_API_KEY=your_actual_api_key_here${NC}\n"
    echo -e "${YELLOW}Then run this script again.${NC}"
    exit 1
else
    echo -e "${GREEN}✓ .env file found${NC}"
fi

# Check if YOUTUBE_API_KEY is set
source .env
if [ -z "$YOUTUBE_API_KEY" ] || [ "$YOUTUBE_API_KEY" = "your_youtube_api_key" ]; then
    echo -e "${RED}✗ YOUTUBE_API_KEY not set in .env${NC}"
    echo -e "${YELLOW}Please edit .env and add your actual YouTube API key${NC}"
    exit 1
else
    echo -e "${GREEN}✓ YouTube API key configured${NC}"
fi

# Check if uvx is available
if ! command -v uvx &> /dev/null; then
    echo -e "${RED}✗ uvx not found${NC}"
    echo -e "${YELLOW}Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
else
    echo -e "${GREEN}✓ uvx found at $(which uvx)${NC}"
fi

echo ""
echo -e "${BLUE}Select a test to run:${NC}"
echo "1. Test server startup (basic check)"
echo "2. Search for videos"
echo "3. Get video details"
echo "4. Get video transcript"
echo "5. Get trending videos"
echo "6. Run MCP Inspector (interactive web UI)"
echo "7. Run comprehensive test suite"
echo "8. Exit"
echo ""

read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo -e "\n${BLUE}Testing server startup...${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}\n"
        uvx --directory . run server.py
        ;;
    2)
        echo -e "\n${BLUE}Searching for videos about 'MCP'...${NC}\n"
        uvx --directory . run client.py search_videos query="MCP" max_results=5
        ;;
    3)
        echo -e "\n${BLUE}Getting details for Rick Astley video...${NC}\n"
        uvx --directory . run client.py get_video_details video_id=dQw4w9WgXcQ
        ;;
    4)
        echo -e "\n${BLUE}Getting transcript for Rick Astley video...${NC}\n"
        uvx --directory . run client.py get_video_transcript video_id=dQw4w9WgXcQ language=en
        ;;
    5)
        echo -e "\n${BLUE}Getting trending videos in US...${NC}\n"
        uvx --directory . run client.py get_trending_videos region_code=US max_results=5
        ;;
    6)
        echo -e "\n${BLUE}Starting MCP Inspector...${NC}"
        echo -e "${YELLOW}This will open a web interface for testing${NC}\n"
        npx -y @modelcontextprotocol/inspector uvx --directory . run server.py
        ;;
    7)
        echo -e "\n${BLUE}Running comprehensive test suite...${NC}"
        echo -e "${YELLOW}Installing Rich library for better output...${NC}\n"
        uvx --directory . pip install rich
        echo -e "\n${BLUE}Running tests...${NC}\n"
        uvx --directory . run test_server.py
        ;;
    8)
        echo -e "${GREEN}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Test completed!${NC}"

