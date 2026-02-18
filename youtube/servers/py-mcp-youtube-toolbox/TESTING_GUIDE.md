# YouTube Toolbox MCP Server - Testing Guide

## Prerequisites

Before testing, ensure you have:

1. **Python 3.12+** installed
2. **uvx** installed (you already have this at `/Users/kennethliao/.local/bin/uvx`)
3. **YouTube API Key** from Google Cloud Console

## Setup Steps

### 1. Create `.env` file

```bash
cd ai_launchpad/claude_code_module/ai-launchpad-marketplace/yt-content-strategist/servers/py-mcp-youtube-toolbox
cp env.example .env
```

Then edit `.env` and add your YouTube API key:
```
YOUTUBE_API_KEY=your_actual_api_key_here
```

### 2. Install Dependencies

The server uses `uv` for dependency management. Install dependencies:

```bash
# Using uvx (recommended)
uvx --directory . pip install -r requirements.txt

# Or if you have uv installed
uv pip install -r requirements.txt
```

## Testing Methods

### Method 1: Quick Test with MCP Inspector

The MCP Inspector provides a web UI to test your server:

```bash
# Run the MCP inspector
npx -y @modelcontextprotocol/inspector uvx --directory . run server.py
```

This will:
- Start the MCP server
- Open a web interface (usually at http://localhost:5173)
- Allow you to test all tools, resources, and prompts interactively

### Method 2: Run the Server Directly

Test if the server starts without errors:

```bash
uvx --directory . run server.py
```

You should see log output indicating the server is ready.

### Method 3: Use the Built-in Client

The repository includes a `client.py` for testing individual tools:

```bash
# Search for videos
uvx --directory . run client.py search_videos query="MCP" max_results=5

# Get video details
uvx --directory . run client.py get_video_details video_id=dQw4w9WgXcQ

# Get channel details
uvx --directory . run client.py get_channel_details channel_id=UCuAXFkgsw1L7xaCfnd5JJOw

# Get video transcript
uvx --directory . run client.py get_video_transcript video_id=dQw4w9WgXcQ language=en

# Get trending videos
uvx --directory . run client.py get_trending_videos region_code=US max_results=5
```

### Method 4: Run Comprehensive Test Suite

I've created a comprehensive test script that tests all functionality:

```bash
# First, install the Rich library for better output
uvx --directory . pip install rich

# Run the test suite
uvx --directory . run test_server.py
```

This will:
- Test all 8 tools
- Test MCP resources
- Display results in a formatted table
- Show which tests passed/failed

## Testing Individual Components

### Test Tools

The server provides these tools:

1. **search_videos** - Search YouTube with filters
2. **get_video_details** - Get video metadata
3. **get_channel_details** - Get channel information
4. **get_video_comments** - Retrieve comments
5. **get_video_transcript** - Get video captions/transcripts
6. **get_related_videos** - Find related content
7. **get_trending_videos** - Get trending videos by region
8. **get_video_enhanced_transcript** - Advanced transcript extraction

### Test Resources

The server exposes these MCP resources:

1. `youtube://available-youtube-tools` - List all tools
2. `youtube://video/{video_id}` - Get video details
3. `youtube://channel/{channel_id}` - Get channel details
4. `youtube://transcript/{video_id}?language={language}` - Get transcript

### Test Prompts

The server provides this prompt:

1. **transcript_summary** - Generate video summaries from transcripts

## Common Issues & Solutions

### Issue: "YOUTUBE_API_KEY environment variable is not set"

**Solution:** Create a `.env` file with your API key (see Setup Steps above)

### Issue: "Module not found" errors

**Solution:** Install dependencies:
```bash
uvx --directory . pip install -r requirements.txt
```

### Issue: "No transcript available"

**Solution:** Not all videos have transcripts. Try these test videos:
- `dQw4w9WgXcQ` - Rick Astley (has English transcript)
- Use videos you know have captions enabled

### Issue: API quota exceeded

**Solution:** YouTube API has daily quotas. If exceeded:
- Wait 24 hours for quota reset
- Use a different API key
- Reduce the number of test requests

## Verifying the Server Works

A successful test should show:

1. ✓ Server starts without errors
2. ✓ Can search for videos
3. ✓ Can retrieve video details
4. ✓ Can get channel information
5. ✓ Can fetch transcripts (for videos that have them)
6. ✓ Can get comments
7. ✓ Can find trending videos

## Next Steps

Once testing is complete:

1. **Configure in Claude Desktop** - Add to `claude_desktop_config.json`
2. **Configure in Cursor** - Add to `.cursor/mcp.json`
3. **Use in your plugin** - The `.mcp.json` in the plugin directory is already configured

## Example: Testing with uvx

Here's the complete command to run the server with uvx:

```bash
# Navigate to the server directory
cd ai_launchpad/claude_code_module/ai-launchpad-marketplace/yt-content-strategist/servers/py-mcp-youtube-toolbox

# Run the server
uvx --directory . run server.py
```

The `--directory .` flag tells uvx to:
1. Look for `pyproject.toml` in the current directory
2. Install dependencies from that file
3. Run the server in an isolated environment

## Debugging

To see detailed logs:

```bash
# Check the log file
tail -f logs/youtube_toolbox.log
```

The server logs all operations to `logs/youtube_toolbox.log` with timestamps and error details.

