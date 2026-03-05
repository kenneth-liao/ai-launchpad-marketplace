# YouTube Data API v3 Reference

Curated reference for agent context. Covers only the endpoints and features used by `youtube_api.py`.

## Authentication

All requests require an API key passed as the `key` parameter. The script reads from:

1. `YOUTUBE_API_KEY` environment variable
2. `~/.claude/.env` file (loaded via python-dotenv)
3. Local `.env` file (fallback)

**Get a key:** [Google Cloud Console](https://console.cloud.google.com/apis/credentials) → Create Credentials → API Key → Restrict to "YouTube Data API v3".

## Endpoints Used

### Search: `GET /youtube/v3/search`

Search for videos, channels, or playlists.

**Key parameters:**
| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search query |
| `part` | string | Always `snippet` |
| `type` | string | `video`, `channel`, `playlist` |
| `maxResults` | int | 1-50 (default: 5) |
| `order` | string | `relevance`, `date`, `rating`, `viewCount`, `title` |
| `channelId` | string | Filter by channel |
| `videoDuration` | string | `short` (<4min), `medium` (4-20min), `long` (>20min) |
| `publishedAfter` | string | RFC 3339 datetime |
| `publishedBefore` | string | RFC 3339 datetime |
| `regionCode` | string | ISO 3166-1 alpha-2 country code |

**Quota cost:** 100 units per request.

### Videos: `GET /youtube/v3/videos`

Get video details by ID.

**Key parameters:**
| Parameter | Type | Description |
|---|---|---|
| `id` | string | Comma-separated video IDs |
| `part` | string | `snippet,contentDetails,statistics` |
| `chart` | string | `mostPopular` (for trending) |
| `regionCode` | string | For trending videos |
| `maxResults` | int | For trending (1-50) |

**Response fields (snippet):** title, description, publishedAt, channelId, channelTitle, tags, thumbnails, categoryId.

**Response fields (statistics):** viewCount, likeCount, commentCount.

**Response fields (contentDetails):** duration (ISO 8601, e.g. `PT4M13S`), dimension, definition.

**Quota cost:** 1 unit per request.

### Channels: `GET /youtube/v3/channels`

Get channel details by ID.

**Key parameters:**
| Parameter | Type | Description |
|---|---|---|
| `id` | string | Channel ID |
| `part` | string | `snippet,statistics` |

**Response fields (snippet):** title, description, publishedAt, customUrl, thumbnails.

**Response fields (statistics):** subscriberCount, videoCount, viewCount.

**Quota cost:** 1 unit per request.

### Comment Threads: `GET /youtube/v3/commentThreads`

Get top-level comments for a video.

**Key parameters:**
| Parameter | Type | Description |
|---|---|---|
| `videoId` | string | Video ID |
| `part` | string | `snippet` or `snippet,replies` |
| `maxResults` | int | 1-100 (default: 20) |
| `order` | string | `relevance` or `time` |
| `pageToken` | string | For pagination |

**Quota cost:** 1 unit per request.

## Transcripts (youtube-transcript-api)

Transcripts are fetched using the `youtube-transcript-api` Python library, NOT the YouTube Data API. This library scrapes the caption tracks directly and does not consume API quota.

**Key behaviors:**
- Tries manual captions in the requested language first
- Falls back to auto-generated captions
- Final fallback to English captions
- Returns a list of segments with `text`, `start` (seconds), and `duration` (seconds)

**Common errors:**
- `TranscriptsDisabled` — Video owner disabled captions
- `NoTranscriptFound` — No captions in the requested language

## Rate Limits and Quotas

### API Key Quotas
- **Default daily quota:** 10,000 units
- **Quota reset:** Midnight Pacific Time
- **Search requests:** 100 units each (most expensive)
- **All other requests:** 1 unit each

### Quota Budget Examples
| Operation | Units | Budget for 10,000 |
|---|---|---|
| Search | 100 | 100 searches/day |
| Video details | 1 | 10,000 videos/day |
| Channel details | 1 | 10,000 channels/day |
| Comments | 1 | 10,000 requests/day |
| Trending | 1 | 10,000 requests/day |

### Rate Limiting
- HTTP 429 or 403 with `quotaExceeded` reason
- The script retries automatically: 3 attempts with exponential backoff (2s, 4s, 8s)
- If quota is fully exhausted, wait until midnight PT

## Response Pagination

List endpoints return pagination tokens:
- `nextPageToken` — Pass as `pageToken` to get next page
- `prevPageToken` — Pass to get previous page
- `pageInfo.totalResults` — Total matching results
- `pageInfo.resultsPerPage` — Results per page

## Video ID Formats

The script's `parse_video_id()` function handles:
- Plain ID: `dQw4w9WgXcQ`
- Full URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Short URL: `https://youtu.be/dQw4w9WgXcQ`
- Embed URL: `https://www.youtube.com/embed/dQw4w9WgXcQ`

## ISO 8601 Duration Format

Video durations are returned in ISO 8601 format:
- `PT4M13S` = 4 minutes, 13 seconds
- `PT1H2M30S` = 1 hour, 2 minutes, 30 seconds
- `PT45S` = 45 seconds
