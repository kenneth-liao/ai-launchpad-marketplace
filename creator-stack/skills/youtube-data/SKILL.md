---
name: youtube-data
description: "Retrieve YouTube data using the YouTube Data API. Use when you need to search videos, get video/channel details, fetch transcripts, read comments, or discover trending/related content."
---

# YouTube Data

Retrieve data from the YouTube Data API v3. Supports searching videos, fetching video/channel details, reading transcripts and comments, and discovering trending or related content.

**Core principle:** Data retrieval only — this skill fetches and returns structured data. It does not produce written content or visual assets.

## When to Use

- Search YouTube for videos matching a query or criteria
- Get detailed statistics for a specific video or channel
- Fetch video transcripts/captions for analysis
- Read and analyze video comments
- Find videos related to a specific video
- Discover trending videos by region
- Extract enhanced transcripts with time filtering, search, and segmentation

## Prerequisites

- `YOUTUBE_API_KEY` — Set in environment or `~/.claude/.env`. Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- [`uv`](https://docs.astral.sh/uv/) (recommended) or Python 3.10+ with dependencies installed

**With `uv` (recommended — zero setup):**
Dependencies are declared inline via PEP 723 and auto-installed on first run. Just use `uv run`.

**With pip (fallback):**
```bash
pip install -r <skill_dir>/requirements.txt
```

## Quick Start

### Search for videos:
```bash
uv run <skill_dir>/scripts/youtube_api.py search "python tutorial" --max-results 5
```

### Get video details:
```bash
uv run <skill_dir>/scripts/youtube_api.py video "dQw4w9WgXcQ"
```

### Get transcript:
```bash
uv run <skill_dir>/scripts/youtube_api.py transcript "dQw4w9WgXcQ" --language en
```

### Get channel info:
```bash
uv run <skill_dir>/scripts/youtube_api.py channel "UC_x5XG1OV2P6uZZ5FSM9Ttw"
```

### Get comments:
```bash
uv run <skill_dir>/scripts/youtube_api.py comments "dQw4w9WgXcQ" --max-results 10 --include-replies
```

### Find related videos:
```bash
uv run <skill_dir>/scripts/youtube_api.py related "dQw4w9WgXcQ" --max-results 5
```

### Get trending videos:
```bash
uv run <skill_dir>/scripts/youtube_api.py trending --region US --max-results 10
```

### Enhanced multi-video transcript:
```bash
uv run <skill_dir>/scripts/youtube_api.py enhanced-transcript "vid1" "vid2" \
  --format merged --include-metadata --language en
```

## Script Reference

### `scripts/youtube_api.py`

Self-contained YouTube Data API script with 8 subcommands.

#### Subcommands

| Subcommand | Description |
|---|---|
| `search` | Search for YouTube videos with advanced filtering |
| `video` | Get detailed information about a video |
| `channel` | Get detailed information about a channel |
| `comments` | Get comments for a video |
| `transcript` | Get transcript/captions for a video |
| `related` | Get videos related to a specific video |
| `trending` | Get trending videos by region |
| `enhanced-transcript` | Advanced multi-video transcript with filtering |

#### `search`

```
youtube_api.py search QUERY [OPTIONS]

Arguments:
  QUERY                          Search query string

Options:
  --max-results N                Number of results (default: 10, max: 50)
  --channel-id ID                Filter by channel
  --order ORDER                  Sort: date, rating, viewCount, relevance, title
  --duration DURATION            Filter: short (<4min), medium (4-20min), long (>20min)
  --published-after DATE         ISO date filter (e.g. 2024-01-01T00:00:00Z)
  --published-before DATE        ISO date filter
  --region CODE                  ISO country code (e.g. US, GB, JP)
```

#### `video`

```
youtube_api.py video VIDEO_ID
```

Returns: title, description, publish date, channel, tags, view/like/comment counts, duration, thumbnails.

#### `channel`

```
youtube_api.py channel CHANNEL_ID
```

Returns: title, description, subscriber/video/view counts, custom URL, thumbnails.

#### `comments`

```
youtube_api.py comments VIDEO_ID [OPTIONS]

Options:
  --max-results N                Number of comments (default: 20)
  --order ORDER                  Sort: relevance (default) or time
  --include-replies              Include reply threads
  --page-token TOKEN             Pagination token
```

#### `transcript`

```
youtube_api.py transcript VIDEO_ID [OPTIONS]

Options:
  --language CODE                Language code (e.g. en, ko, fr)
```

Returns: timestamped segments and full text with timestamps.

#### `related`

```
youtube_api.py related VIDEO_ID [OPTIONS]

Options:
  --max-results N                Number of results (default: 10)
```

#### `trending`

```
youtube_api.py trending [OPTIONS]

Options:
  --region CODE                  ISO country code (default: US)
  --max-results N                Number of results (default: 5)
```

#### `enhanced-transcript`

```
youtube_api.py enhanced-transcript VIDEO_ID [VIDEO_ID...] [OPTIONS]

Arguments:
  VIDEO_IDS                      One or more video IDs (max 5)

Options:
  --language CODE                Language code
  --format FORMAT                Output: raw, timestamped (default), merged
  --start-time SECONDS           Filter from this time
  --end-time SECONDS             Filter until this time
  --search QUERY                 Search within transcript text
  --case-sensitive               Case-sensitive search
  --segment-method METHOD        Segmentation: equal (default), smart
  --segment-count N              Number of segments (default: 1)
  --include-metadata             Include video details with transcript
```

### Return Structure

All subcommands output JSON to stdout with this consistent structure:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "metadata": {
    "timestamp": "2025-01-26T12:00:00",
    ...
  }
}
```

On failure, `success` is `false`, `data` is `null`, and `error` contains the message. Exit code is `0` on success, `1` on failure.

## Python API

### Direct import (from another skill's script):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("<skill_dir>/scripts")))
from youtube_api import search_videos, get_video_details, get_video_transcript

# Search videos
result = search_videos("python tutorial", max_results=5)

# Get video details
result = get_video_details("dQw4w9WgXcQ")

# Get transcript
result = get_video_transcript("dQw4w9WgXcQ", language="en")
```

### Available functions:

| Function | Description |
|---|---|
| `search_videos(query, ...)` | Search YouTube videos |
| `get_video_details(video_id)` | Get video details |
| `get_channel_details(channel_id)` | Get channel details |
| `get_video_comments(video_id, ...)` | Get video comments |
| `get_video_transcript(video_id, ...)` | Get video transcript |
| `get_related_videos(video_id, ...)` | Get related videos |
| `get_trending_videos(region, ...)` | Get trending videos |
| `get_enhanced_transcript(video_ids, ...)` | Enhanced multi-video transcript |

All functions return the same `{success, data, error, metadata}` dict.

## Downstream Skill Integration

### Pattern 1: CLI wrapper (recommended for agents)

```bash
result=$(uv run <skill_dir>/scripts/youtube_api.py search "AI tutorials" --max-results 5)
echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['items'][0]['title'])"
```

### Pattern 2: Python import with custom defaults

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-api-python-client>=2.169.0",
#     "youtube-transcript-api>=1.0.3",
#     "python-dotenv>=1.1.0",
# ]
# ///

import sys
from pathlib import Path
sys.path.insert(0, str(Path("<skill_dir>/scripts")))
from youtube_api import search_videos, get_video_transcript

def research_topic(topic: str, count: int = 10) -> list:
    """Search and get transcripts for top videos on a topic."""
    search_result = search_videos(topic, max_results=count)
    if not search_result["success"]:
        return []
    videos = search_result["data"]["items"]
    for v in videos:
        t = get_video_transcript(v["videoId"], language="en")
        v["transcript"] = t["data"]["text"] if t["success"] else None
    return videos
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `YOUTUBE_API_KEY` | YouTube Data API v3 key | Required |

## Troubleshooting

**"uv: command not found"**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`

**"Required packages not installed"**
- Use `uv run` instead of `python3` to auto-install dependencies
- Or install manually: `pip install -r <skill_dir>/requirements.txt`

**"YOUTUBE_API_KEY environment variable not set"**
- Set `YOUTUBE_API_KEY` in your shell, `~/.claude/.env`, or local `.env`

**"HttpError 403: quotaExceeded"**
- YouTube Data API has a daily quota (default 10,000 units)
- Wait until quota resets or request a quota increase
- The script retries rate-limited requests automatically (3 attempts with exponential backoff)

**"No transcript available"**
- Video may not have captions enabled
- Try a different `--language` code
- Auto-generated captions may be available in other languages

## References

- [references/youtube-data-api.md](./references/youtube-data-api.md) — YouTube Data API v3 endpoints, quotas, and response structures
