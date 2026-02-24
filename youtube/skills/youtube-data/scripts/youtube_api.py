#!/usr/bin/env python3
"""
YouTube Data API - Self-contained script for YouTube data retrieval.

Supports searching videos, fetching details, transcripts, comments,
and discovering trending/related content.

Usage:
    uv run youtube_api.py search "python tutorial" --max-results 5
    uv run youtube_api.py video "dQw4w9WgXcQ"
    uv run youtube_api.py transcript "dQw4w9WgXcQ" --language en
    uv run youtube_api.py channel "UC_x5XG1OV2P6uZZ5FSM9Ttw"
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-api-python-client>=2.169.0",
#     "youtube-transcript-api>=1.0.3",
#     "python-dotenv>=1.1.0",
# ]
# ///

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from youtube_transcript_api import (
        NoTranscriptFound,
        TranscriptsDisabled,
        YouTubeTranscriptApi,
    )
except ImportError:
    print("Error: Required packages not installed.")
    print("Run this script with: uv run youtube_api.py <args>")
    print("Or install manually: pip install -r requirements.txt")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Environment / API key
# ---------------------------------------------------------------------------

# Load from ~/.claude/.env first, then local .env as fallback
_claude_env = os.path.join(os.path.expanduser("~"), ".claude", ".env")
if os.path.exists(_claude_env):
    load_dotenv(_claude_env, override=True)
load_dotenv()


def _get_api_key() -> str:
    """Return YOUTUBE_API_KEY or raise."""
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        raise ValueError(
            "YOUTUBE_API_KEY environment variable not set. "
            "Get a key at: https://console.cloud.google.com/apis/credentials"
        )
    return key


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MAX_RETRIES = 3
BASE_DELAY = 2  # seconds


def _retry_on_rate_limit(func):
    """Decorator: exponential backoff on HTTP 429 / quota errors."""

    def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except HttpError as e:
                if e.resp.status in (429, 403) and attempt < MAX_RETRIES - 1:
                    delay = BASE_DELAY * (2 ** attempt)
                    print(
                        f"Rate limited (attempt {attempt + 1}/{MAX_RETRIES}), "
                        f"retrying in {delay}s...",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                else:
                    raise
        return None  # unreachable

    return wrapper


def _ok(data: Any, **meta) -> dict:
    """Build a success response."""
    return {
        "success": True,
        "data": data,
        "error": None,
        "metadata": {"timestamp": datetime.now().isoformat(), **meta},
    }


def _err(message: str, **meta) -> dict:
    """Build an error response."""
    return {
        "success": False,
        "data": None,
        "error": message,
        "metadata": {"timestamp": datetime.now().isoformat(), **meta},
    }


def parse_video_id(url_or_id: str) -> str:
    """Extract a video ID from a YouTube URL (or return the ID as-is)."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
    return match.group(1) if match else url_or_id


def _normalize_region(code: Optional[str]) -> Optional[str]:
    """Normalise common non-standard region codes to ISO 3166-1 alpha-2."""
    if not code:
        return None
    mapping = {"KO": "KR", "EN": "US", "JP": "JP", "CN": "CN"}
    return mapping.get(code.upper(), code.upper())


def _format_time(seconds: float) -> str:
    """Format seconds into HH:MM:SS or MM:SS."""
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# YouTubeService - core API wrapper
# ---------------------------------------------------------------------------

class YouTubeService:
    """Thin wrapper around the YouTube Data API v3."""

    def __init__(self, api_key: str):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    # -- search --
    @_retry_on_rate_limit
    def search_videos(self, query: str, max_results: int = 10, **opts) -> dict:
        params: dict[str, Any] = {
            "part": "snippet",
            "q": query,
            "maxResults": max_results,
            "type": opts.get("type", "video"),
        }
        for key in (
            "channelId", "order", "videoDuration",
            "publishedAfter", "publishedBefore",
            "videoCaption", "videoDefinition", "regionCode",
        ):
            if opts.get(key):
                params[key] = opts[key]
        return self.youtube.search().list(**params).execute()

    # -- video details --
    @_retry_on_rate_limit
    def get_video_details(self, video_id: str) -> dict:
        video_id = parse_video_id(video_id)
        return self.youtube.videos().list(
            part="snippet,contentDetails,statistics", id=video_id
        ).execute()

    # -- channel details --
    @_retry_on_rate_limit
    def get_channel_details(self, channel_id: str) -> dict:
        return self.youtube.channels().list(
            part="snippet,statistics", id=channel_id
        ).execute()

    # -- comments --
    @_retry_on_rate_limit
    def get_video_comments(self, video_id: str, max_results: int = 20, **opts) -> dict:
        video_id = parse_video_id(video_id)
        params: dict[str, Any] = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": max_results,
        }
        if opts.get("order"):
            params["order"] = opts["order"]
        if opts.get("pageToken"):
            params["pageToken"] = opts["pageToken"]
        if opts.get("includeReplies"):
            params["part"] = "snippet,replies"
        return self.youtube.commentThreads().list(**params).execute()

    # -- transcript --
    def get_video_transcript(self, video_id: str, language: Optional[str] = None) -> list:
        video_id = parse_video_id(video_id)
        ytt = YouTubeTranscriptApi()
        if language:
            transcript_list = ytt.list(video_id)
            try:
                transcript = transcript_list.find_transcript([language])
                return transcript.fetch().to_raw_data()
            except NoTranscriptFound:
                try:
                    transcript = transcript_list.find_generated_transcript([language])
                    return transcript.fetch().to_raw_data()
                except Exception:
                    transcript = transcript_list.find_transcript(["en"])
                    return transcript.fetch().to_raw_data()
        else:
            return ytt.fetch(video_id).to_raw_data()

    # -- related videos --
    @_retry_on_rate_limit
    def get_related_videos(self, video_id: str, max_results: int = 10) -> dict:
        video_id = parse_video_id(video_id)
        details = self.get_video_details(video_id)
        if not details.get("items"):
            raise ValueError(f"Video {video_id} not found")
        title = details["items"][0]["snippet"]["title"]
        search_query = " ".join(title.split()[:3])
        response = self.youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            maxResults=max_results,
            relevanceLanguage="en",
        ).execute()
        if "items" in response:
            response["items"] = [
                i for i in response["items"]
                if i.get("id", {}).get("videoId") != video_id
            ]
        response["searchQuery"] = search_query
        return response

    # -- trending --
    @_retry_on_rate_limit
    def get_trending_videos(self, region_code: Optional[str] = None, max_results: int = 5) -> dict:
        params: dict[str, Any] = {
            "part": "snippet,contentDetails,statistics",
            "chart": "mostPopular",
            "maxResults": max_results,
        }
        if region_code:
            params["regionCode"] = _normalize_region(region_code)
        return self.youtube.videos().list(**params).execute()


# ---------------------------------------------------------------------------
# Public API functions  (importable + called by CLI)
# ---------------------------------------------------------------------------

def search_videos(
    query: str,
    max_results: int = 10,
    channel_id: Optional[str] = None,
    order: Optional[str] = None,
    duration: Optional[str] = None,
    published_after: Optional[str] = None,
    published_before: Optional[str] = None,
    region: Optional[str] = None,
) -> dict:
    """Search YouTube videos. Returns standardised response dict."""
    try:
        svc = YouTubeService(_get_api_key())
        raw = svc.search_videos(
            query, max_results,
            channelId=channel_id, order=order,
            videoDuration=duration,
            publishedAfter=published_after,
            publishedBefore=published_before,
            regionCode=region,
        )
        items = []
        for item in raw.get("items", []):
            vid = item.get("id", {}).get("videoId")
            items.append({
                "videoId": vid,
                "title": item["snippet"].get("title"),
                "channelId": item["snippet"].get("channelId"),
                "channelTitle": item["snippet"].get("channelTitle"),
                "publishedAt": item["snippet"].get("publishedAt"),
                "description": item["snippet"].get("description"),
                "thumbnails": item["snippet"].get("thumbnails"),
                "url": f"https://www.youtube.com/watch?v={vid}",
            })
        return _ok(
            {"items": items, "totalResults": raw.get("pageInfo", {}).get("totalResults", 0),
             "nextPageToken": raw.get("nextPageToken")},
            query=query, max_results=max_results,
        )
    except Exception as e:
        return _err(str(e), query=query)


def get_video_details(video_id: str) -> dict:
    """Get detailed info about a YouTube video."""
    try:
        svc = YouTubeService(_get_api_key())
        raw = svc.get_video_details(video_id)
        if not raw.get("items"):
            return _err(f"Video {video_id} not found", video_id=video_id)
        v = raw["items"][0]
        details = {
            "id": v.get("id"),
            "title": v["snippet"].get("title"),
            "description": v["snippet"].get("description"),
            "publishedAt": v["snippet"].get("publishedAt"),
            "channelId": v["snippet"].get("channelId"),
            "channelTitle": v["snippet"].get("channelTitle"),
            "tags": v["snippet"].get("tags", []),
            "viewCount": v.get("statistics", {}).get("viewCount"),
            "likeCount": v.get("statistics", {}).get("likeCount"),
            "commentCount": v.get("statistics", {}).get("commentCount"),
            "duration": v.get("contentDetails", {}).get("duration"),
            "definition": v.get("contentDetails", {}).get("definition"),
            "thumbnails": v["snippet"].get("thumbnails"),
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }
        return _ok(details, video_id=video_id)
    except Exception as e:
        return _err(str(e), video_id=video_id)


def get_channel_details(channel_id: str) -> dict:
    """Get detailed info about a YouTube channel."""
    try:
        svc = YouTubeService(_get_api_key())
        raw = svc.get_channel_details(channel_id)
        if not raw.get("items"):
            return _err(f"Channel {channel_id} not found", channel_id=channel_id)
        ch = raw["items"][0]
        details = {
            "id": ch.get("id"),
            "title": ch["snippet"].get("title"),
            "description": ch["snippet"].get("description"),
            "publishedAt": ch["snippet"].get("publishedAt"),
            "customUrl": ch["snippet"].get("customUrl"),
            "thumbnails": ch["snippet"].get("thumbnails"),
            "subscriberCount": ch.get("statistics", {}).get("subscriberCount"),
            "videoCount": ch.get("statistics", {}).get("videoCount"),
            "viewCount": ch.get("statistics", {}).get("viewCount"),
            "url": f"https://www.youtube.com/channel/{channel_id}",
        }
        return _ok(details, channel_id=channel_id)
    except Exception as e:
        return _err(str(e), channel_id=channel_id)


def get_video_comments(
    video_id: str,
    max_results: int = 20,
    order: str = "relevance",
    include_replies: bool = False,
    page_token: Optional[str] = None,
) -> dict:
    """Get comments for a YouTube video."""
    try:
        svc = YouTubeService(_get_api_key())
        opts: dict[str, Any] = {"order": order, "includeReplies": include_replies}
        if page_token:
            opts["pageToken"] = page_token
        raw = svc.get_video_comments(video_id, max_results, **opts)
        comments = []
        for item in raw.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            c: dict[str, Any] = {
                "id": item.get("id"),
                "text": snippet.get("textDisplay"),
                "author": snippet.get("authorDisplayName"),
                "likeCount": snippet.get("likeCount"),
                "publishedAt": snippet.get("publishedAt"),
                "replyCount": item["snippet"].get("totalReplyCount", 0),
            }
            if include_replies and "replies" in item:
                c["replies"] = [
                    {
                        "id": r.get("id"),
                        "text": r["snippet"].get("textDisplay"),
                        "author": r["snippet"].get("authorDisplayName"),
                        "likeCount": r["snippet"].get("likeCount"),
                        "publishedAt": r["snippet"].get("publishedAt"),
                    }
                    for r in item["replies"].get("comments", [])
                ]
            comments.append(c)
        return _ok(
            {"comments": comments, "nextPageToken": raw.get("nextPageToken"),
             "totalResults": raw.get("pageInfo", {}).get("totalResults", 0)},
            video_id=video_id,
        )
    except Exception as e:
        return _err(str(e), video_id=video_id)


def get_video_transcript(video_id: str, language: Optional[str] = None) -> dict:
    """Get transcript/captions for a YouTube video."""
    try:
        svc = YouTubeService(_get_api_key())
        # Fetch video metadata
        vraw = svc.get_video_details(video_id)
        title = None
        channel = None
        if vraw.get("items"):
            v = vraw["items"][0]
            title = v["snippet"].get("title")
            channel = v["snippet"].get("channelTitle")

        raw = svc.get_video_transcript(video_id, language)
        segments = []
        for seg in raw:
            text = seg.get("text", "")
            start = seg.get("start", 0)
            dur = seg.get("duration", 0)
            segments.append({
                "text": text,
                "start": start,
                "duration": dur,
                "timestamp": _format_time(start),
            })
        timestamped = "\n".join(f"[{s['timestamp']}] {s['text']}" for s in segments)
        return _ok(
            {"transcript": segments, "text": timestamped},
            video_id=video_id, title=title, channel=channel,
            language=language or "default", segment_count=len(segments),
        )
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        return _err(f"No transcript available: {e}", video_id=video_id)
    except Exception as e:
        return _err(str(e), video_id=video_id)


def get_related_videos(video_id: str, max_results: int = 10) -> dict:
    """Get videos related to a specific YouTube video."""
    try:
        svc = YouTubeService(_get_api_key())
        raw = svc.get_related_videos(video_id, max_results)
        items = []
        for item in raw.get("items", []):
            vid = item.get("id", {}).get("videoId")
            items.append({
                "videoId": vid,
                "title": item["snippet"].get("title"),
                "channelTitle": item["snippet"].get("channelTitle"),
                "publishedAt": item["snippet"].get("publishedAt"),
                "description": item["snippet"].get("description"),
                "thumbnails": item["snippet"].get("thumbnails"),
                "url": f"https://www.youtube.com/watch?v={vid}",
            })
        return _ok(
            {"videos": items, "totalResults": len(items),
             "searchQuery": raw.get("searchQuery", "")},
            video_id=video_id,
        )
    except Exception as e:
        return _err(str(e), video_id=video_id)


def get_trending_videos(region: Optional[str] = None, max_results: int = 5) -> dict:
    """Get trending videos for a region."""
    try:
        svc = YouTubeService(_get_api_key())
        raw = svc.get_trending_videos(region, max_results)
        items = []
        for v in raw.get("items", []):
            items.append({
                "id": v.get("id"),
                "title": v["snippet"].get("title"),
                "description": v["snippet"].get("description"),
                "publishedAt": v["snippet"].get("publishedAt"),
                "channelId": v["snippet"].get("channelId"),
                "channelTitle": v["snippet"].get("channelTitle"),
                "viewCount": v.get("statistics", {}).get("viewCount"),
                "likeCount": v.get("statistics", {}).get("likeCount"),
                "commentCount": v.get("statistics", {}).get("commentCount"),
                "thumbnails": v["snippet"].get("thumbnails"),
                "url": f"https://www.youtube.com/watch?v={v.get('id')}",
            })
        return _ok(
            {"videos": items, "totalResults": len(items)},
            region=region or "US",
        )
    except Exception as e:
        return _err(str(e), region=region)


def get_enhanced_transcript(
    video_ids: List[str],
    language: Optional[str] = None,
    format: str = "timestamped",
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    search: Optional[str] = None,
    case_sensitive: bool = False,
    segment_method: str = "equal",
    segment_count: int = 1,
    include_metadata: bool = False,
) -> dict:
    """Enhanced transcript extraction with filtering, search, and multi-video support."""
    if not video_ids:
        return _err("No video IDs provided")
    if len(video_ids) > 5:
        return _err("Maximum 5 video IDs allowed")

    svc = YouTubeService(_get_api_key())
    videos = []
    success_count = 0
    fail_count = 0

    for vid in video_ids:
        vid = parse_video_id(vid)
        entry: dict[str, Any] = {"videoId": vid}
        try:
            # metadata
            if include_metadata:
                vraw = svc.get_video_details(vid)
                if not vraw.get("items"):
                    entry["error"] = f"Video {vid} not found"
                    videos.append(entry)
                    fail_count += 1
                    continue
                v = vraw["items"][0]
                entry["metadata"] = {
                    "id": v.get("id"),
                    "title": v["snippet"].get("title"),
                    "channelTitle": v["snippet"].get("channelTitle"),
                    "publishedAt": v["snippet"].get("publishedAt"),
                    "duration": v.get("contentDetails", {}).get("duration"),
                }

            # transcript
            raw = svc.get_video_transcript(vid, language)
            if not raw:
                entry["error"] = "Failed to retrieve transcript"
                videos.append(entry)
                fail_count += 1
                continue

            segments = []
            for seg in raw:
                text = getattr(seg, "text", "") if not isinstance(seg, dict) else seg.get("text", "")
                start = getattr(seg, "start", 0) if not isinstance(seg, dict) else seg.get("start", 0)
                dur = getattr(seg, "duration", 0) if not isinstance(seg, dict) else seg.get("duration", 0)
                segments.append({
                    "text": text, "start": start, "duration": dur,
                    "timestamp": _format_time(start),
                })

            # time range filter
            if start_time is not None:
                segments = [s for s in segments if (s["start"] + s["duration"]) >= start_time]
            if end_time is not None:
                segments = [s for s in segments if s["start"] <= end_time]

            # search filter
            if search and segments:
                q = search if case_sensitive else search.lower()
                matched = []
                for i, s in enumerate(segments):
                    t = s["text"] if case_sensitive else s["text"].lower()
                    if q in t:
                        matched.append(i)
                # add 2 context lines
                expanded = set()
                for idx in matched:
                    for j in range(max(0, idx - 2), min(len(segments), idx + 3)):
                        expanded.add(j)
                segments = [segments[i] for i in sorted(expanded)]

            # segmentation
            if segment_count > 1 and segments:
                seg_size = len(segments) // segment_count
                seg_list = []
                for i in range(segment_count):
                    start_idx = i * seg_size
                    end_idx = start_idx + seg_size if i < segment_count - 1 else len(segments)
                    chunk = segments[start_idx:end_idx]
                    if chunk:
                        seg_list.append({
                            "index": i,
                            "segments": chunk,
                            "text": " ".join(s["text"] for s in chunk),
                        })
                entry["segments"] = seg_list

            # format
            if format == "raw":
                entry["transcript"] = segments
            elif format == "merged":
                entry["transcript"] = " ".join(s["text"] for s in segments)
            else:  # timestamped
                entry["transcript"] = [f"[{s['timestamp']}] {s['text']}" for s in segments]

            entry["statistics"] = {
                "segmentCount": len(segments),
                "totalDuration": sum(s["duration"] for s in segments),
                "averageSegmentLength": (
                    sum(len(s["text"]) for s in segments) / len(segments)
                    if segments else 0
                ),
            }
            videos.append(entry)
            success_count += 1

        except Exception as e:
            entry["error"] = str(e)
            videos.append(entry)
            fail_count += 1

    if fail_count == 0:
        msg = "Transcripts processed successfully"
    elif success_count == 0:
        msg = "All transcript requests failed"
    else:
        msg = f"Partially successful ({fail_count} failed, {success_count} succeeded)"

    return _ok(
        {"videos": videos, "status": {
            "successCount": success_count, "failedCount": fail_count, "message": msg,
        }},
        video_ids=video_ids, format=format,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="YouTube Data API - search, details, transcripts, and more",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search "python tutorial" --max-results 5
  %(prog)s video "dQw4w9WgXcQ"
  %(prog)s channel "UC_x5XG1OV2P6uZZ5FSM9Ttw"
  %(prog)s comments "dQw4w9WgXcQ" --max-results 10
  %(prog)s transcript "dQw4w9WgXcQ" --language en
  %(prog)s related "dQw4w9WgXcQ"
  %(prog)s trending --region US --max-results 10
  %(prog)s enhanced-transcript "vid1" "vid2" --format merged
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- search ---
    p = sub.add_parser("search", help="Search for YouTube videos")
    p.add_argument("query", help="Search query")
    p.add_argument("--max-results", type=int, default=10)
    p.add_argument("--channel-id")
    p.add_argument("--order", choices=["date", "rating", "viewCount", "relevance", "title"])
    p.add_argument("--duration", choices=["short", "medium", "long"])
    p.add_argument("--published-after", help="ISO date (e.g. 2024-01-01T00:00:00Z)")
    p.add_argument("--published-before", help="ISO date")
    p.add_argument("--region", help="ISO country code (e.g. US)")

    # --- video ---
    p = sub.add_parser("video", help="Get video details")
    p.add_argument("video_id", help="YouTube video ID or URL")

    # --- channel ---
    p = sub.add_parser("channel", help="Get channel details")
    p.add_argument("channel_id", help="YouTube channel ID")

    # --- comments ---
    p = sub.add_parser("comments", help="Get video comments")
    p.add_argument("video_id", help="YouTube video ID or URL")
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--order", choices=["relevance", "time"], default="relevance")
    p.add_argument("--include-replies", action="store_true")
    p.add_argument("--page-token")

    # --- transcript ---
    p = sub.add_parser("transcript", help="Get video transcript")
    p.add_argument("video_id", help="YouTube video ID or URL")
    p.add_argument("--language", help="Language code (e.g. en, ko)")

    # --- related ---
    p = sub.add_parser("related", help="Get related videos")
    p.add_argument("video_id", help="YouTube video ID or URL")
    p.add_argument("--max-results", type=int, default=10)

    # --- trending ---
    p = sub.add_parser("trending", help="Get trending videos")
    p.add_argument("--region", default="US", help="ISO country code (default: US)")
    p.add_argument("--max-results", type=int, default=5)

    # --- enhanced-transcript ---
    p = sub.add_parser("enhanced-transcript", help="Enhanced multi-video transcript")
    p.add_argument("video_ids", nargs="+", help="YouTube video IDs (max 5)")
    p.add_argument("--language", help="Language code")
    p.add_argument("--format", choices=["raw", "timestamped", "merged"], default="timestamped")
    p.add_argument("--start-time", type=int, help="Start time in seconds")
    p.add_argument("--end-time", type=int, help="End time in seconds")
    p.add_argument("--search", help="Search query within transcript")
    p.add_argument("--case-sensitive", action="store_true")
    p.add_argument("--segment-method", choices=["equal", "smart"], default="equal")
    p.add_argument("--segment-count", type=int, default=1)
    p.add_argument("--include-metadata", action="store_true")

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    dispatch = {
        "search": lambda a: search_videos(
            a.query, a.max_results,
            channel_id=a.channel_id, order=a.order, duration=a.duration,
            published_after=a.published_after, published_before=a.published_before,
            region=a.region,
        ),
        "video": lambda a: get_video_details(a.video_id),
        "channel": lambda a: get_channel_details(a.channel_id),
        "comments": lambda a: get_video_comments(
            a.video_id, a.max_results, a.order, a.include_replies, a.page_token,
        ),
        "transcript": lambda a: get_video_transcript(a.video_id, a.language),
        "related": lambda a: get_related_videos(a.video_id, a.max_results),
        "trending": lambda a: get_trending_videos(a.region, a.max_results),
        "enhanced-transcript": lambda a: get_enhanced_transcript(
            a.video_ids, language=a.language, format=a.format,
            start_time=a.start_time, end_time=a.end_time,
            search=a.search, case_sensitive=a.case_sensitive,
            segment_method=a.segment_method, segment_count=a.segment_count,
            include_metadata=a.include_metadata,
        ),
    }

    result = dispatch[args.command](args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
