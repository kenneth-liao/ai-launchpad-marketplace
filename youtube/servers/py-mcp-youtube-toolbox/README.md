# py-mcp-youtube-toolbox
[![smithery badge](https://smithery.ai/badge/@jikime/py-mcp-youtube-toolbox)](https://smithery.ai/server/@jikime/py-mcp-youtube-toolbox) ![](https://badge.mcpx.dev?type=server 'MCP Server') ![Version](https://img.shields.io/badge/version-1.0.0-green) ![License](https://img.shields.io/badge/license-MIT-blue)

An MCP server that provides AI assistants with powerful tools to interact with YouTube, including video searching, transcript extraction, comment retrieval, and more.

<a href="https://glama.ai/mcp/servers/@jikime/py-mcp-youtube-toolbox">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@jikime/py-mcp-youtube-toolbox/badge" alt="YouTube Toolbox MCP server" />
</a>

## Overview

py-mcp-youtube-toolbox provides the following YouTube-related functionalities:

- Search YouTube videos with advanced filtering options
- Get detailed information about videos and channels
- Retrieve video comments with sorting options
- Extract video transcripts and captions in multiple languages
- Find related videos for a given video
- Get trending videos by region
- Generate summaries of video content based on transcripts
- Advanced transcript analysis with filtering, searching, and multi-video capabilities

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configure MCP Settings](#configure-mcp-settings)
- [Tools Documentation](#tools-documentation)
  - [Video Tools](#video-tools)
  - [Channel Tools](#channel-tools)
  - [Transcript Tools](#transcript-tools)
  - [Prompt Tools](#prompt-tools)
  - [Resource Tools](#resource-tools)
- [Development](#development)
- [License](#license)

## Prerequisites
1. **Python**: Install Python 3.12 or higher
2. **YouTube API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3:
     1. Go to "APIs & Services" > "Library"
     2. Search for and enable "YouTube Data API v3"
   - Create credentials:
     1. Go to "APIs & Services" > "Credentials"
     2. Click "Create Credentials" > "API key"
     3. Note down your API key

## Installation
#### Git Clone
```bash
git clone https://github.com/jikime/py-mcp-youtube-toolbox.git
cd py-mcp-youtube-toolbox
```

#### Configuration 
1. Install UV package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate virtual environment:
```bash
uv venv -p 3.12
source .venv/bin/activate  # On MacOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Environment variables:
```bash
cp env.example .env
vi .env
# Update with your YouTube API key
YOUTUBE_API_KEY=your_youtube_api_key
```

#### Using Docker

1. Build the Docker image:
```bash
docker build -t py-mcp-youtube-toolbox .
```

2. Run the container:
```bash
docker run -e YOUTUBE_API_KEY=your_youtube_api_key py-mcp-youtube-toolbox
```

#### Using Local

1. Run the server:
```bash
mcp run server.py
```

2. Run the MCP Inspector:
```bash
mcp dev server.py
```

## Configure MCP Settings
Add the server configuration to your MCP settings file:

#### Claude desktop app 
1. To install automatically via [Smithery](https://smithery.ai/server/@jikime/py-mcp-youtube-toolbox):

```bash
npx -y @smithery/cli install @jikime/py-mcp-youtube-toolbox --client claude
```

2. To install manually
open `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this to the `mcpServers` object:
```json
{
  "mcpServers": {
    "YouTube Toolbox": {
      "command": "/path/to/bin/uv",
      "args": [
        "--directory",
        "/path/to/py-mcp-youtube-toolbox",
        "run",
        "server.py"
      ],
      "env": {
        "YOUTUBE_API_KEY": "your_youtube_api_key"
      }
    }
  }
}
```

#### Cursor IDE 
open `~/.cursor/mcp.json`

Add this to the `mcpServers` object:
```json
{
  "mcpServers": {
    "YouTube Toolbox": {
      "command": "/path/to/bin/uv",
      "args": [
        "--directory",
        "/path/to/py-mcp-youtube-toolbox",
        "run",
        "server.py"
      ],
      "env": {
        "YOUTUBE_API_KEY": "your_youtube_api_key"
      }
    }
  }
}
```

#### for Docker
```json
{
  "mcpServers": {
    "YouTube Toolbox": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "YOUTUBE_API_KEY=your_youtube_api_key",
        "py-mcp-youtube-toolbox"
      ]
    }
  }
}
```

## Tools Documentation

### Video Tools

- `search_videos`: Search for YouTube videos with advanced filtering options (channel, duration, region, etc.)
- `get_video_details`: Get detailed information about a specific YouTube video (title, channel, views, likes, etc.)
- `get_video_comments`: Retrieve comments from a YouTube video with sorting options
- `get_related_videos`: Find videos related to a specific YouTube video
- `get_trending_videos`: Get trending videos on YouTube by region

### Channel Tools

- `get_channel_details`: Get detailed information about a YouTube channel (name, subscribers, views, etc.)

### Transcript Tools

- `get_video_transcript`: Extract transcripts/captions from YouTube videos in specified languages
- `get_video_enhanced_transcript`: Advanced transcript extraction with filtering, search, and multi-video capabilities

### Prompt Tools

- `transcript_summary`: Generate summaries of YouTube video content based on transcripts with customizable options

### Resource Tools

- `youtube://available-youtube-tools`: Get a list of all available YouTube tools
- `youtube://video/{video_id}`: Get detailed information about a specific video
- `youtube://channel/{channel_id}`: Get information about a specific channel
- `youtube://transcript/{video_id}?language={language}`: Get transcript for a specific video

## Development

For local testing, you can use the included client script:

```bash
# Example: Search videos
uv run client.py search_videos query="MCP" max_results=5

# Example: Get video details
uv run client.py get_video_details video_id=zRgAEIoZEVQ

# Example: Get channel details
uv run client.py get_channel_details channel_id=UCRpOIr-NJpK9S483ge20Pgw

# Example: Get video comments
uv run client.py get_video_comments video_id=zRgAEIoZEVQ max_results=10 order=time

# Example: Get video transcript
uv run client.py get_video_transcript video_id=zRgAEIoZEVQ language=ko

# Example: Get related videos
uv run client.py get_related_videos video_id=zRgAEIoZEVQ max_results=5

# Example: Get trending videos
uv run client.py get_trending_videos region_code=ko max_results=10

# Example: Advanced transcript extraction
uv run client.py get_video_enhanced_transcript video_ids=zRgAEIoZEVQ language=ko format=timestamped include_metadata=true start_time=100 end_time=200 query=에이전트 case_sensitive=true segment_method=equal segment_count=2

# Example: 
```

## License

MIT License



docker run --env-file .env py-mcp-youtube-toolbox

npx -y @modelcontextprotocol/inspector npx <package-name> <args>

# For example

npx -y @modelcontextprotocol/inspector npx /Users/kennethliao/projects/MCP/py-mcp-youtube-toolbox/server.py 