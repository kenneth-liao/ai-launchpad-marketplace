#!/usr/bin/env python3
import os
import json
import re
import logging
from logging.handlers import RotatingFileHandler
from typing import List, Dict, Any, Optional

# pydantic imports
from dotenv import load_dotenv

# Google API related imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YouTube transcript API

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# MCP related imports
from mcp.server.fastmcp import FastMCP

# Load environment variables
# Cross-platform path to ~/.claude/.env
claude_env_path = os.path.join(os.path.expanduser("~"), ".claude", ".env")
if os.path.exists(claude_env_path):
    load_dotenv(claude_env_path, override=True)

# Also check local .env as fallback
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create log directory
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "youtube_toolbox.log")

# Add file handler
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Check if YOUTUBE_API_KEY is available
if not YOUTUBE_API_KEY:
    logger.error("YOUTUBE_API_KEY environment variable is not set")
    raise ValueError("YOUTUBE_API_KEY environment variable is required")

# Create MCP server
mcp = FastMCP("YouTube Toolbox MCP Server")
logger.info("YouTube Toolbox MCP Server 준비 중...")

# Define prompt
@mcp.prompt(
    name="transcript_summary",
    description="Generate a summary of a YouTube video based on its transcript content with customizable options. This prompt provides different summary levels from brief overviews to detailed analyses, and can extract key topics from the content. Optimal for quickly understanding video content without watching the entire video."
)
async def transcript_summary(
    video_id: str,
    language: Optional[str] = None,
    summary_length: Optional[str] = None,
    include_keywords: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a summary of a YouTube video based on its transcript content with customizable options
    
    Args:
        video_id (str): The YouTube video ID
        language (str, optional): Language code for transcript (e.g., "en", "ko")
        summary_length (str, optional): Level of detail in summary ("short", "medium", or "detailed", default: "medium")
        include_keywords (str, optional): Whether to extract key topics (set to "true" to enable)
    
    Returns:
        Dict[str, Any]: Prompt configuration for the LLM
    """
    try:
        # Set defaults
        final_summary_length = summary_length or 'medium'
        should_include_keywords = include_keywords == 'true'
        
        # Get video details and transcript
        video_data = youtube_service.get_video_details(video_id)
        if not video_data or 'error' in video_data:
            return {
                'messages': [{
                    'role': 'user',
                    'content': f"Error: Could not retrieve video details for ID {video_id}"
                }]
            }
            
        video = video_data['items'][0] if 'items' in video_data and video_data['items'] else None
        
        # Get transcript data
        try:
            raw_transcript_data = youtube_service.get_video_transcript(video_id, language)
            
            # Format transcript text based on the actual structure
            transcript_text = ""
            
            if isinstance(raw_transcript_data, dict):
                # Handle dictionary response (might have transcript or text key)
                if 'transcript' in raw_transcript_data:
                    transcript_text = ' '.join([segment.get('text', '') for segment in raw_transcript_data['transcript']])
                elif 'text' in raw_transcript_data:
                    transcript_text = raw_transcript_data['text']
            elif isinstance(raw_transcript_data, list):
                # Handle list response (direct list of segment dictionaries)
                transcript_text = ' '.join([item.get('text', '') for item in raw_transcript_data])
            else:
                # Handle FetchedTranscript objects or other types
                transcript_segments = []
                for segment in raw_transcript_data:
                    text = getattr(segment, 'text', '')
                    transcript_segments.append(text)
                transcript_text = ' '.join(transcript_segments)
            
            if not transcript_text:
                return {
                    'messages': [{
                        'role': 'user',
                        'content': f"Error: Could not extract transcript text for video ID {video_id}."
                    }]
                }
                
        except Exception as e:
            logger.exception(f"Error getting transcript for video {video_id}: {e}")
            return {
                'messages': [{
                    'role': 'user',
                    'content': f"Error: Could not retrieve transcript for video ID {video_id}. {str(e)}"
                }]
            }
        
        # Define summary instructions based on length
        summary_instructions = ''
        if final_summary_length == 'short':
            summary_instructions = "Please provide a brief summary of this video in 3-5 sentences that captures the main idea."
        elif final_summary_length == 'detailed':
            summary_instructions = """Please provide a comprehensive summary of this video, including:
1. A detailed overview of the main topics (at least 3-4 paragraphs)
2. All important details, facts, and arguments presented
3. The structure of the content and how ideas are developed
4. The overall tone, style, and intended audience of the content
5. Any conclusions or calls to action mentioned"""
        else:  # 'medium' or default
            summary_instructions = """Please provide:
1. A concise summary of the main topics and key points
2. Important details or facts presented
3. The overall tone and style of the content"""
        
        # Add keywords extraction if requested
        if should_include_keywords:
            summary_instructions += """\n\nAlso extract and list 5-10 key topics, themes, or keywords from the content in the format:
KEY TOPICS: [comma-separated list of key topics/keywords]"""
        
        # Get video metadata
        video_title = video.get('snippet', {}).get('title', 'Unknown') if video else 'Unknown'
        channel_title = video.get('snippet', {}).get('channelTitle', 'Unknown') if video else 'Unknown'
        published_at = video.get('snippet', {}).get('publishedAt', 'Unknown') if video else 'Unknown'
        
        # Construct the prompt message
        prompt_message = f"""Please provide a {final_summary_length} summary of the following YouTube video transcript.

Video Title: {video_title}
Channel: {channel_title}
Published: {published_at}

Transcript:
{transcript_text}

{summary_instructions}"""
        
        return {
            'messages': [{
                'role': 'user',
                'content': prompt_message
            }]
        }
    except Exception as e:
        logger.exception(f"Error in transcript_summary prompt: {e}")
        return {
            'messages': [{
                'role': 'user',
                'content': f"Error creating transcript summary prompt: {str(e)}"
            }]
        }

class YouTubeService:
    """Service for interacting with YouTube API"""
    
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
    def parse_url(self, url: str) -> str:
        """
        Parse the URL to get the video ID
        """
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not video_id_match:
            return url
        video_id = video_id_match.group(1)
        
        return video_id
    
    def normalize_region_code(self, region_code: str) -> str:
        """
        Convert region codes to valid ISO 3166-1 alpha-2 country codes
        """
        if not region_code:
            return None
            
        # Common mappings for non-standard codes to standard ISO codes
        region_mapping = {
            'KO': 'KR',  # Korea
            'EN': 'US',  # English -> US as fallback
            'JP': 'JP',  # Japan
            'CN': 'CN',  # China
        }
        
        # Convert to uppercase
        region_code = region_code.upper()
        
        # Return mapped code or original if no mapping exists
        return region_mapping.get(region_code, region_code)
    
    def search_videos(self, query: str, max_results: int = 10, **options) -> Dict[str, Any]:
        """
        Search for YouTube videos based on query and options
        """
        try:
            search_params = {
                'part': 'snippet',
                'q': query,
                'maxResults': max_results,
                'type': options.get('type', 'video')
            }
            
            # Add optional parameters if provided
            for param in ['channelId', 'order', 'videoDuration', 'publishedAfter', 
                        'publishedBefore', 'videoCaption', 'videoDefinition', 'regionCode']:
                if param in options and options[param]:
                    search_params[param] = options[param]
            
            response = self.youtube.search().list(**search_params).execute()
            return response
        except HttpError as e:
            logger.error(f"Error searching videos: {e}")
            raise e
    
    def get_video_details(self, video_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific YouTube video
        """
        video_id = self.parse_url(video_id)
        
        try:
            response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()
            return response
        except HttpError as e:
            logger.error(f"Error getting video details: {e}")
            raise e
    
    def get_channel_details(self, channel_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific YouTube channel
        """
        channel_id = self.parse_url(channel_id)
        
        try:
            response = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            ).execute()
            return response
        except HttpError as e:
            logger.error(f"Error getting channel details: {e}")
            raise e
    
    def get_video_comments(self, video_id: str, max_results: int = 20, **options) -> Dict[str, Any]:
        """
        Get comments for a specific YouTube video
        """
        video_id = self.parse_url(video_id)
        
        try:
            params = {
                'part': 'snippet',
                'videoId': video_id,
                'maxResults': max_results
            }
            
            if 'order' in options:
                params['order'] = options['order']
                
            if 'pageToken' in options:
                params['pageToken'] = options['pageToken']
                
            if options.get('includeReplies'):
                params['part'] = 'snippet,replies'
                
            response = self.youtube.commentThreads().list(**params).execute()
            return response
        except HttpError as e:
            logger.error(f"Error getting comments: {e}")
            raise e
    
    def get_video_transcript(self, video_id: str, language: Optional[str] = 'ko') -> List[Dict[str, Any]]:
        """
        Get transcript for a specific YouTube video
        """
        video_id = self.parse_url(video_id)
        
        try:
            if language:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                try:
                    transcript = transcript_list.find_transcript([language])
                    return transcript.fetch()
                except NoTranscriptFound:
                    # Fallback to generated transcript if available
                    try:
                        transcript = transcript_list.find_generated_transcript([language])
                        return transcript.fetch()
                    except:
                        # Final fallback to any available transcript
                        transcript = transcript_list.find_transcript(['en'])
                        return transcript.fetch()
            else:
                return YouTubeTranscriptApi.get_video_transcript(video_id)
                
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            logger.error(f"No transcript available for video {video_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting transcript for video {video_id}: {e}")
            raise e

    def get_related_videos(self, video_id: str, max_results: Optional[int] = 10) -> Dict[str, Any]:
        """
        Get related videos for a specific YouTube video
        """
        video_id = self.parse_url(video_id)
        
        try:
            # Use search to find videos for a similar query to effectively get related content
            # First, get video details to use title for search
            video_details = self.get_video_details(video_id)
            if not video_details.get('items'):
                raise ValueError(f"Video with ID {video_id} not found")
            
            video_title = video_details['items'][0]['snippet']['title']
            # Extract a few keywords from the title for search
            search_query = ' '.join(video_title.split()[:3]) if video_title else ''
            
            # Search for videos with similar content
            response = self.youtube.search().list(
                part='snippet',
                q=search_query,
                type='video',
                maxResults=max_results,
                videoCategoryId=video_details['items'][0]['snippet'].get('categoryId', ''),
                relevanceLanguage='en'  # Can be adjusted based on requirements
            ).execute()
            
            # Filter out the original video from results
            if 'items' in response:
                response['items'] = [item for item in response['items'] 
                                    if item.get('id', {}).get('videoId') != video_id]
                # Adjust result count if original video was filtered
                if len(response['items']) < max_results:
                    response['pageInfo']['totalResults'] = len(response['items'])
                    response['pageInfo']['resultsPerPage'] = len(response['items'])
            
            # Add the search query to the response for reference
            response['searchQuery'] = search_query
            
            return response
        except HttpError as e:
            logger.error(f"Error getting related videos: {e}")
            raise e
          
            
    def get_trending_videos(self, region_code: Optional[str] = 'ko', max_results: Optional[int] = 5) -> Dict[str, Any]:
        """
        Get trending videos for a specific region
        """
        try:
            params = {
                'part': 'snippet,contentDetails,statistics',
                'chart': 'mostPopular',
                'maxResults': max_results
            }
            
            if region_code:
                # Normalize region code to ensure valid ISO country code format
                normalized_code = self.normalize_region_code(region_code)
                params['regionCode'] = normalized_code
                
            response = self.youtube.videos().list(**params).execute()
            return response
        except HttpError as e:
            logger.error(f"Error getting trending videos: {e}")
            raise e
            
    def format_time(self, milliseconds: int) -> str:
        """
        Format milliseconds into a human-readable time string
        """
        seconds = int(milliseconds / 1000)
        minutes = int(seconds / 60)
        hours = int(minutes / 60)
        
        remaining_seconds = seconds % 60
        remaining_minutes = minutes % 60
        
        if hours > 0:
            return f"{hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"
        else:
            return f"{remaining_minutes:02d}:{remaining_seconds:02d}"

    def get_video_enhanced_transcript(self, video_ids: List[str], options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get enhanced transcript for one or more YouTube videos with advanced filtering and processing
        
        Args:
            video_ids (List[str]): List of YouTube video IDs
            options (Dict[str, Any]): Advanced options for transcript processing
                - language (str, optional): Language code
                - format (str, optional): Output format (raw, timestamped, merged)
                - includeMetadata (bool, optional): Whether to include video details
                - timeRange (Dict, optional): Time range filter with start and end in seconds
                - search (Dict, optional): Search filter with query, caseSensitive, and contextLines
                - segment (Dict, optional): Segmentation options with method and count
                
        Returns:
            Dict[str, Any]: Enhanced transcript data
        """
        result = {
            "videos": [],
            "status": {
                "success": True,
                "message": "Transcripts processed successfully",
                "failedCount": 0,
                "successCount": 0
            }
        }
        
        # Process options
        language = options.get('language')
        format_type = options.get('format', 'timestamped')
        include_metadata = options.get('includeMetadata', False)
        time_range = options.get('timeRange')
        search_filter = options.get('search')
        segment_options = options.get('segment')
        
        # Process each video
        for video_id in video_ids:
            video_result = {"videoId": video_id}
            
            try:
                # Get video details if metadata requested
                if include_metadata:
                    video_data = self.get_video_details(video_id)
                    if not video_data.get('items'):
                        video_result["error"] = f"Video with ID {video_id} not found"
                        result["videos"].append(video_result)
                        result["status"]["failedCount"] += 1
                        continue
                        
                    video = video_data['items'][0]
                    video_result["metadata"] = {
                        'id': video.get('id'),
                        'title': video.get('snippet', {}).get('title'),
                        'channelTitle': video.get('snippet', {}).get('channelTitle'),
                        'publishedAt': video.get('snippet', {}).get('publishedAt'),
                        'duration': video.get('contentDetails', {}).get('duration')
                    }
                
                # Call the get_video_transcript method which returns transcript data
                raw_transcript_data = self.get_video_transcript(video_id, language)
                
                # Check if transcript was fetched successfully
                if not raw_transcript_data or (isinstance(raw_transcript_data, dict) and 'error' in raw_transcript_data):
                    error_msg = raw_transcript_data.get('error', "Failed to retrieve transcript") if isinstance(raw_transcript_data, dict) else "Failed to retrieve transcript"
                    video_result["error"] = error_msg
                    result["videos"].append(video_result)
                    result["status"]["failedCount"] += 1
                    continue
                
                # Get transcript segments - adapt to different response formats
                if isinstance(raw_transcript_data, dict) and 'transcript' in raw_transcript_data:
                    # If it's a dictionary with transcript key (from existing get_video_transcript method)
                    segments = raw_transcript_data['transcript']
                elif isinstance(raw_transcript_data, dict) and 'text' in raw_transcript_data:
                    # If the get_video_transcript method returned a formatted response with 'text'
                    # This is a fallback case
                    segments = []
                    video_result["error"] = "Transcript format not supported"
                    result["videos"].append(video_result)
                    result["status"]["failedCount"] += 1
                    continue
                elif isinstance(raw_transcript_data, list):
                    # If it returned a list directly (might happen in some cases)
                    segments = []
                    for item in raw_transcript_data:
                        segments.append({
                            'text': item.get('text', ''),
                            'start': item.get('start', 0),
                            'duration': item.get('duration', 0),
                            'timestamp': self.format_time(int(item.get('start', 0) * 1000))
                        })
                else:
                    # This handles the FetchedTranscript objects from YouTubeTranscriptApi
                    # that don't have a .get() method
                    segments = []
                    for segment in raw_transcript_data:
                        text = getattr(segment, 'text', '')
                        start = getattr(segment, 'start', 0)
                        duration = getattr(segment, 'duration', 0)
                        
                        segments.append({
                            'text': text,
                            'start': start,
                            'duration': duration,
                            'timestamp': self.format_time(int(start * 1000))
                        })
                
                # Apply time range filter if specified
                if time_range:
                    start_time = time_range.get('start')
                    end_time = time_range.get('end')
                    
                    if start_time is not None:
                        segments = [s for s in segments if (s['start'] + s['duration']) >= start_time]
                    
                    if end_time is not None:
                        segments = [s for s in segments if s['start'] <= end_time]
                
                # Apply search filter if specified
                if search_filter and segments:
                    query = search_filter.get('query', '')
                    case_sensitive = search_filter.get('caseSensitive', False)
                    context_lines = search_filter.get('contextLines', 0)
                    
                    if query:
                        # Search in segments
                        matched_indices = []
                        search_query = query if case_sensitive else query.lower()
                        
                        for i, segment in enumerate(segments):
                            text = segment['text'] if case_sensitive else segment['text'].lower()
                            if search_query in text:
                                matched_indices.append(i)
                        
                        # Include context lines
                        if context_lines > 0:
                            expanded_indices = set()
                            for idx in matched_indices:
                                # Add the context lines before and after
                                for i in range(max(0, idx - context_lines), min(len(segments), idx + context_lines + 1)):
                                    expanded_indices.add(i)
                            
                            matched_indices = sorted(expanded_indices)
                        
                        # Filter segments by matched indices
                        segments = [segments[i] for i in matched_indices]
                
                # Apply segmentation if specified
                if segment_options and segments:
                    method = segment_options.get('method', 'equal')
                    count = segment_options.get('count', 1)
                    
                    if method == 'equal' and count > 1:
                        # Divide into equal parts
                        segment_size = len(segments) // count
                        segmented_transcript = []
                        
                        for i in range(count):
                            start_idx = i * segment_size
                            end_idx = start_idx + segment_size if i < count - 1 else len(segments)
                            
                            segment_chunks = segments[start_idx:end_idx]
                            if segment_chunks:  # Only add non-empty segments
                                segmented_transcript.append({
                                    "index": i,
                                    "segments": segment_chunks,
                                    "text": " ".join([s['text'] for s in segment_chunks])
                                })
                        
                        video_result["segments"] = segmented_transcript
                    elif method == 'smart' and count > 1:
                        # Use a smarter segmentation approach
                        # For simplicity, we'll use a basic approach dividing by total character count
                        total_text = " ".join([s['text'] for s in segments])
                        total_chars = len(total_text)
                        chars_per_segment = total_chars // count
                        
                        segmented_transcript = []
                        current_segment = []
                        current_chars = 0
                        segment_idx = 0
                        
                        for s in segments:
                            current_segment.append(s)
                            current_chars += len(s['text'])
                            
                            if current_chars >= chars_per_segment and segment_idx < count - 1:
                                segmented_transcript.append({
                                    "index": segment_idx,
                                    "segments": current_segment,
                                    "text": " ".join([seg['text'] for seg in current_segment])
                                })
                                segment_idx += 1
                                current_segment = []
                                current_chars = 0
                        
                        # Add the last segment if not empty
                        if current_segment:
                            segmented_transcript.append({
                                "index": segment_idx,
                                "segments": current_segment,
                                "text": " ".join([seg['text'] for seg in current_segment])
                            })
                        
                        video_result["segments"] = segmented_transcript
                
                # Format transcript based on format type
                if format_type == 'raw':
                    video_result["transcript"] = segments
                elif format_type == 'timestamped':
                    video_result["transcript"] = [
                        f"[{s['timestamp']}] {s['text']}" for s in segments
                    ]
                elif format_type == 'merged':
                    video_result["transcript"] = " ".join([s['text'] for s in segments])
                
                # Store statistics
                video_result["statistics"] = {
                    "segmentCount": len(segments),
                    "totalDuration": sum([s['duration'] for s in segments]),
                    "averageSegmentLength": sum([len(s['text']) for s in segments]) / len(segments) if segments else 0
                }
                
                result["videos"].append(video_result)
                result["status"]["successCount"] += 1
                
            except Exception as e:
                logger.exception(f"Error processing transcript for video {video_id}: {e}")
                video_result["error"] = str(e)
                result["videos"].append(video_result)
                result["status"]["failedCount"] += 1
        
        # Update overall status
        if result["status"]["failedCount"] > 0:
            if result["status"]["successCount"] == 0:
                result["status"]["success"] = False
                result["status"]["message"] = "All transcript requests failed"
            else:
                result["status"]["message"] = f"Partially successful ({result['status']['failedCount']} failed, {result['status']['successCount']} succeeded)"
        
        return result

# Initialize YouTube service
youtube_service = YouTubeService()

# Define resource
@mcp.resource(
    uri='youtube://available-youtube-tools', 
    name="available-youtube-tools", 
    description="Returns a list of YouTube tools available on this MCP server."
)
async def get_available_youtube_tools() -> List[Dict[str, str]]:
    """Returns a list of YouTube tools available on this MCP server."""
    available_tools = [
        {"name": "search_videos", "description": "Search for YouTube videos with advanced filtering options"},
        {"name": "get_video_details", "description": "Get detailed information about a YouTube video"},
        {"name": "get_channel_details", "description": "Get detailed information about a YouTube channel"},
        {"name": "get_video_comments", "description": "Get comments for a YouTube video"},
        {"name": "get_video_transcript", "description": "Get transcript/captions for a YouTube video"},
        {"name": "get_related_videos", "description": "Get videos related to a specific YouTube video"},
        {"name": "get_trending_videos", "description": "Get trending videos on YouTube by region"},
        {"name": "get_video_enhanced_transcript", "description": "Advanced transcript extraction tool with filtering, search, and multi-video capabilities. Provides rich transcript data for detailed analysis and processing. Features: 1) Extract transcripts from multiple videos; 2) Filter by time ranges; 3) Search within transcripts; 4) Segment transcripts; 5) Format output in different ways; 6) Include video metadata."}
    ]
    
    logger.info(f"Resource 'get_available_youtube_tools' called. Returning {len(available_tools)} tools.")
    return available_tools

@mcp.resource(
    uri='youtube://video/{video_id}',
    name="video",
    description="Get detailed information about a specific YouTube video by ID"
)
async def get_video_resource(video_id: str) -> str:
    """
    Resource for getting detailed information about a specific YouTube video
    
    Args:
        video_id (str): YouTube video ID
    
    Returns:
        Dict[str, Any]: Video details resource
    """

    try:
        video_data = youtube_service.get_video_details(video_id)
        
        if not video_data.get('items'):
            return {
                "contents": [{
                    "uri": f"youtube://video/{video_id}",
                    "text": f"Video with ID {video_id} not found."
                }]
            }
            
        video = video_data['items'][0]
        
        # Format the response
        details = {
            'id': video.get('id'),
            'title': video.get('snippet', {}).get('title'),
            'description': video.get('snippet', {}).get('description'),
            'publishedAt': video.get('snippet', {}).get('publishedAt'),
            'channelId': video.get('snippet', {}).get('channelId'),
            'channelTitle': video.get('snippet', {}).get('channelTitle'),
            'viewCount': video.get('statistics', {}).get('viewCount'),
            'likeCount': video.get('statistics', {}).get('likeCount'),
            'commentCount': video.get('statistics', {}).get('commentCount'),
            'duration': video.get('contentDetails', {}).get('duration')
        }
        
        return {
            "contents": [{
                "uri": f"youtube://video/{video_id}",
                "text": json.dumps(details, indent=2)
            }]
        }
    except Exception as e:
        logger.exception(f"Error in get_video_details: {e}")
        return {
            "contents": [{
                "uri": f"youtube://video/{video_id}",
                "text": f"Error fetching video details: {str(e)}"
            }]
        }

@mcp.resource(
    uri='youtube://channel/{channel_id}',
    name="channel",
    description="Get information about a specific YouTube channel by ID"
)
async def get_channel_resource(channel_id: str) -> Dict[str, Any]:
    """
    Resource for getting information about a specific YouTube channel
    
    Args:
        channel_id (str): YouTube channel ID
    
    Returns:
        Dict[str, Any]: Channel details resource
    """
    try:
        channel_data = youtube_service.get_channel_details(channel_id)
        
        if not channel_data.get('items'):
            return {
                "contents": [{
                    "uri": f"youtube://channel/{channel_id}",
                    "text": f"Channel with ID {channel_id} not found."
                }]
            }
            
        channel = channel_data['items'][0]
        
        # Format the response
        details = {
            'id': channel.get('id'),
            'title': channel.get('snippet', {}).get('title'),
            'description': channel.get('snippet', {}).get('description'),
            'publishedAt': channel.get('snippet', {}).get('publishedAt'),
            'subscriberCount': channel.get('statistics', {}).get('subscriberCount'),
            'videoCount': channel.get('statistics', {}).get('videoCount'),
            'viewCount': channel.get('statistics', {}).get('viewCount')
        }
        
        return {
            "contents": [{
                "uri": f"youtube://channel/{channel_id}",
                "text": json.dumps(details, indent=2)
            }]
        }
    except Exception as e:
        logger.exception(f"Error in get_channel_resource: {e}")
        return {
            "contents": [{
                "uri": f"youtube://channel/{channel_id}",
                "text": f"Error fetching channel details: {str(e)}"
            }]
        }

@mcp.resource(
    uri='youtube://transcript/{video_id}?language={language}',
    name="transcript",
    description="Get the transcript/captions for a specific YouTube video",
)
async def get_video_transcript_resource(video_id: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Resource for getting transcript/captions for a specific YouTube video
    
    Args:
        video_id (str): YouTube video ID
        language (str, optional): Language code for transcript
    
    Returns:
        Dict[str, Any]: Transcript resource
    """
    try:
        # Get video details for metadata
        video_data = youtube_service.get_video_details(video_id)
        
        if not video_data.get('items'):
            return {
                "contents": [{
                    "uri": f"youtube://transcript/{video_id}",
                    "text": f"Video with ID {video_id} not found."
                }]
            }
            
        video = video_data['items'][0]
        
        try:
            # Get transcript
            transcript_data = youtube_service.get_video_transcript(video_id, language)
            
            # Format transcript with timestamps
            formatted_transcript = []
            for segment in transcript_data:
                # FetchedTranscriptSnippet 객체에서 속성으로 접근
                text = getattr(segment, 'text', '')
                start = getattr(segment, 'start', 0)
                duration = getattr(segment, 'duration', 0)
                
                formatted_transcript.append({
                    'text': text,
                    'start': start,
                    'duration': duration,
                    'timestamp': youtube_service.format_time(int(start * 1000))
                })
            
            # Create metadata
            metadata = {
                'videoId': video.get('id'),
                'title': video.get('snippet', {}).get('title'),
                'channelTitle': video.get('snippet', {}).get('channelTitle'),
                'language': language or 'default',
                'segmentCount': len(transcript_data)
            }
            
            # Create timestamped text version
            timestamped_text = "\n".join([
                f"[{item['timestamp']}] {item['text']}" 
                for item in formatted_transcript
            ])
            
            return {
                "contents": [{
                    "uri": f"youtube://transcript/{video_id}",
                    "text": f"# Transcript for: {metadata['title']}\n\n{timestamped_text}"
                }],
                "metadata": metadata
            }
        except Exception as e:
            return {
                "contents": [{
                    "uri": f"youtube://transcript/{video_id}",
                    "text": f"Transcript not available for video ID {video_id}. Error: {str(e)}"
                }]
            }
    except Exception as e:
        logger.exception(f"Error in get_video_transcript_resource: {e}")
        return {
            "contents": [{
                "uri": f"youtube://transcript/{video_id}",
                "text": f"Error fetching transcript: {str(e)}"
            }]
        }

# Define tools
@mcp.tool(
    name="search_videos",
    description="Search for YouTube videos with advanced filtering options",
)
async def search_videos(
    query: str, 
    max_results: Optional[int] = 10, 
    channel_id: Optional[str] = None,
    order: Optional[str] = None,
    video_duration: Optional[str] = None,
    published_after: Optional[str] = None,
    published_before: Optional[str] = None,
    video_caption: Optional[str] = None,
    video_definition: Optional[str] = None,
    region_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for YouTube videos with advanced filtering options
    
    Args:
        query (str): Search term
        max_results (int): Number of results to return (1-50)
        channel_id (str, optional): Filter by specific channel
        order (str, optional): Sort by date, rating, viewCount, relevance, title
        video_duration (str, optional): Filter by length (short: <4min, medium: 4-20min, long: >20min)
        published_after (str, optional): Filter by publish date after (ISO format)
        published_before (str, optional): Filter by publish date before (ISO format)
        video_caption (str, optional): Filter by caption availability
        video_definition (str, optional): Filter by quality (standard/high)
        region_code (str, optional): Filter by country (ISO country code)
    
    Returns:
        Dict[str, Any]: Search results
    """
    try:
        options = {
            'channelId': channel_id,
            'order': order,
            'videoDuration': video_duration,
            'publishedAfter': published_after,
            'publishedBefore': published_before,
            'videoCaption': video_caption,
            'videoDefinition': video_definition,
            'regionCode': region_code
        }
        
        search_results = youtube_service.search_videos(query, max_results, **options)
        
        # Format the response
        formatted_results = []
        for item in search_results.get('items', []):
            video_id = item.get('id', {}).get('videoId')
            
            formatted_results.append({
                'videoId': video_id,
                'title': item.get('snippet', {}).get('title'),
                'channelId': item.get('snippet', {}).get('channelId'),
                'channelTitle': item.get('snippet', {}).get('channelTitle'),
                'publishedAt': item.get('snippet', {}).get('publishedAt'),
                'description': item.get('snippet', {}).get('description'),
                'thumbnails': item.get('snippet', {}).get('thumbnails'),
                'url': f"https://www.youtube.com/watch?v={video_id}"
            })
            
        return {
            'items': formatted_results,
            'totalResults': search_results.get('pageInfo', {}).get('totalResults', 0),
            'nextPageToken': search_results.get('nextPageToken')
        }
    except Exception as e:
        logger.exception(f"Error in search_videos: {e}")
        return {'error': str(e)}

@mcp.tool(
    name="get_video_details",
    description="Get detailed information about a YouTube video",
)
async def get_video_details(video_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a YouTube video
    
    Args:
        video_id (str): YouTube video ID
    
    Returns:
        Dict[str, Any]: Video details
    """
    try:
        video_data = youtube_service.get_video_details(video_id)
        
        if not video_data.get('items'):
            return {'error': f"Video with ID {video_id} not found"}
            
        video = video_data['items'][0]
        
        # Format the response
        details = {
            'id': video.get('id'),
            'title': video.get('snippet', {}).get('title'),
            'description': video.get('snippet', {}).get('description'),
            'publishedAt': video.get('snippet', {}).get('publishedAt'),
            'channelId': video.get('snippet', {}).get('channelId'),
            'channelTitle': video.get('snippet', {}).get('channelTitle'),
            'tags': video.get('snippet', {}).get('tags', []),
            'viewCount': video.get('statistics', {}).get('viewCount'),
            'likeCount': video.get('statistics', {}).get('likeCount'),
            'commentCount': video.get('statistics', {}).get('commentCount'),
            'duration': video.get('contentDetails', {}).get('duration'),
            'dimension': video.get('contentDetails', {}).get('dimension'),
            'definition': video.get('contentDetails', {}).get('definition'),
            'thumbnails': video.get('snippet', {}).get('thumbnails'),
            'url': f"https://www.youtube.com/watch?v={video_id}"
        }
        
        return details
    except Exception as e:
        logger.exception(f"Error in get_video_details: {e}")
        return {'error': str(e)}

@mcp.tool(
    name="get_channel_details",
    description="Get detailed information about a YouTube channel",
)
async def get_channel_details(channel_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a YouTube channel
    
    Args:
        channel_id (str): YouTube channel ID
    
    Returns:
        Dict[str, Any]: Channel details
    """
    try:
        channel_data = youtube_service.get_channel_details(channel_id)
        
        if not channel_data.get('items'):
            return {'error': f"Channel with ID {channel_id} not found"}
            
        channel = channel_data['items'][0]
        
        # Format the response
        details = {
            'id': channel.get('id'),
            'title': channel.get('snippet', {}).get('title'),
            'description': channel.get('snippet', {}).get('description'),
            'publishedAt': channel.get('snippet', {}).get('publishedAt'),
            'customUrl': channel.get('snippet', {}).get('customUrl'),
            'thumbnails': channel.get('snippet', {}).get('thumbnails'),
            'subscriberCount': channel.get('statistics', {}).get('subscriberCount'),
            'videoCount': channel.get('statistics', {}).get('videoCount'),
            'viewCount': channel.get('statistics', {}).get('viewCount'),
            'url': f"https://www.youtube.com/channel/{channel_id}"
        }
        
        return details
    except Exception as e:
        logger.exception(f"Error in get_channel_details: {e}")
        return {'error': str(e)}

@mcp.tool(
    name="get_video_comments",
    description="Get comments for a YouTube video",
)
async def get_video_comments(
    video_id: str, 
    max_results: Optional[int] = 20, 
    order: Optional[str] = "relevance", 
    include_replies: bool = False,
    page_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get comments for a YouTube video
    
    Args:
        video_id (str): YouTube video ID
        max_results (int): Maximum number of comments to return (default: 20)
        order (str): Order by 'relevance' (default) or 'time'
        include_replies (bool): Whether to include replies to comments
        page_token (str, optional): Token for paginated results
    
    Returns:
        Dict[str, Any]: Comments data
    """
    try:
        options = {
            'order': order,
            'includeReplies': include_replies,
        }
        
        if page_token:
            options['pageToken'] = page_token
            
        comments_data = youtube_service.get_video_comments(video_id, max_results, **options)
        
        # Format the response
        formatted_comments = []
        for item in comments_data.get('items', []):
            comment = item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {})
            
            formatted_comment = {
                'id': item.get('id'),
                'text': comment.get('textDisplay'),
                'author': comment.get('authorDisplayName'),
                'authorProfileImageUrl': comment.get('authorProfileImageUrl'),
                'likeCount': comment.get('likeCount'),
                'publishedAt': comment.get('publishedAt'),
                'updatedAt': comment.get('updatedAt'),
                'replyCount': item.get('snippet', {}).get('totalReplyCount', 0)
            }
            
            # Include replies if requested and available
            if include_replies and 'replies' in item:
                reply_comments = []
                for reply in item.get('replies', {}).get('comments', []):
                    reply_snippet = reply.get('snippet', {})
                    reply_comments.append({
                        'id': reply.get('id'),
                        'text': reply_snippet.get('textDisplay'),
                        'author': reply_snippet.get('authorDisplayName'),
                        'authorProfileImageUrl': reply_snippet.get('authorProfileImageUrl'),
                        'likeCount': reply_snippet.get('likeCount'),
                        'publishedAt': reply_snippet.get('publishedAt'),
                        'updatedAt': reply_snippet.get('updatedAt')
                    })
                
                formatted_comment['replies'] = reply_comments
                
            formatted_comments.append(formatted_comment)
            
        return {
            'comments': formatted_comments,
            'nextPageToken': comments_data.get('nextPageToken'),
            'totalResults': comments_data.get('pageInfo', {}).get('totalResults', 0)
        }
    except Exception as e:
        logger.exception(f"Error in get_video_comments: {e}")
        return {'error': str(e)}

@mcp.tool(
    name="get_video_transcript",
    description="Get transcript/captions for a YouTube video",
)
async def get_video_transcript(video_id: str, language: Optional[str] = 'ko') -> Dict[str, Any]:
    """
    Get transcript/captions for a YouTube video
    
    Args:
        video_id (str): YouTube video ID
        language (str, optional): Language code (e.g., 'en', 'ko', 'fr')
    
    Returns:
        Dict[str, Any]: Transcript data
    """
    try:
        # Get video details for metadata
        video_data = youtube_service.get_video_details(video_id)
        
        if not video_data.get('items'):
            return {'error': f"Video with ID {video_id} not found"}
            
        video = video_data['items'][0]
        
        # Get transcript
        try:
            transcript_data = youtube_service.get_video_transcript(video_id, language)
            
            # Format transcript with timestamps
            formatted_transcript = []
            for segment in transcript_data:
                text = getattr(segment, 'text', '')
                start = getattr(segment, 'start', 0)
                duration = getattr(segment, 'duration', 0)
                
                formatted_transcript.append({
                    'text': text,
                    'start': start,
                    'duration': duration,
                    'timestamp': youtube_service.format_time(int(start * 1000))
                })
            
            # Create metadata
            metadata = {
                'videoId': video.get('id'),
                'title': video.get('snippet', {}).get('title'),
                'channelTitle': video.get('snippet', {}).get('channelTitle'),
                'language': language or 'default',
                'segmentCount': len(transcript_data)
            }
            
            # Create timestamped text version
            timestamped_text = "\n".join([
                f"[{item['timestamp']}] {item['text']}" 
                for item in formatted_transcript
            ])
            
            return {
                'metadata': metadata,
                'transcript': formatted_transcript,
                'text': timestamped_text,
                'channelId': video.get('snippet', {}).get('channelId')
            }
        except Exception as e:
            return {
                'error': f"Could not retrieve transcript: {str(e)}",
                'videoId': video_id,
                'title': video.get('snippet', {}).get('title')
            }
            
    except Exception as e:
        logger.exception(f"Error in get_video_transcript: {e}")
        return {'error': str(e)}

@mcp.tool(
    name="get_related_videos",
    description="Get videos related to a specific YouTube video",
)
async def get_related_videos(video_id: str, max_results: Optional[int] = 10) -> Dict[str, Any]:
    """
    Get videos related to a specific YouTube video
    
    Args:
        video_id (str): YouTube video ID
        max_results (int): Maximum number of related videos to return (default: 10)
    
    Returns:
        Dict[str, Any]: Related videos data
    """
    try:
        related_data = youtube_service.get_related_videos(video_id, max_results)
        
        # Format the response
        formatted_videos = []
        for item in related_data.get('items', []):
            related_video_id = item.get('id', {}).get('videoId')
            
            formatted_videos.append({
                'videoId': related_video_id,
                'title': item.get('snippet', {}).get('title'),
                'channelTitle': item.get('snippet', {}).get('channelTitle'),
                'publishedAt': item.get('snippet', {}).get('publishedAt'),
                'description': item.get('snippet', {}).get('description'),
                'thumbnails': item.get('snippet', {}).get('thumbnails'),
                'url': f"https://www.youtube.com/watch?v={related_video_id}"
            })
            
        return {
            'videos': formatted_videos,
            'totalResults': len(formatted_videos),
            'originalVideoId': video_id,
            'searchQuery': related_data.get('searchQuery', '')
        }
    except Exception as e:
        logger.exception(f"Error in get_related_videos: {e}")
        return {'error': str(e)}

@mcp.tool(
    name="get_trending_videos",
    description="Get trending videos on YouTube by region",
)
async def get_trending_videos(region_code: str = None, max_results: int = 5) -> Dict[str, Any]:
    """
    Get trending videos on YouTube by region
    
    Args:
        region_code (str): ISO country code (default: 'US')
        max_results (int): Maximum number of videos to return (default: 10)
    
    Returns:
        Dict[str, Any]: Trending videos data
    """
    try:
        # 이제 region_code 처리는 YouTubeService 클래스 내부에서 처리합니다
        trending_data = youtube_service.get_trending_videos(region_code, max_results)
        
        # Format the response
        formatted_videos = []
        for video in trending_data.get('items', []):
            formatted_videos.append({
                'id': video.get('id'),
                'title': video.get('snippet', {}).get('title'),
                'description': video.get('snippet', {}).get('description'),
                'publishedAt': video.get('snippet', {}).get('publishedAt'),
                'channelId': video.get('snippet', {}).get('channelId'),
                'channelTitle': video.get('snippet', {}).get('channelTitle'),
                'viewCount': video.get('statistics', {}).get('viewCount'),
                'likeCount': video.get('statistics', {}).get('likeCount'),
                'commentCount': video.get('statistics', {}).get('commentCount'),
                'thumbnails': video.get('snippet', {}).get('thumbnails'),
                'url': f"https://www.youtube.com/watch?v={video.get('id')}"
            })
            
        return {
            'videos': formatted_videos,
            'region': region_code,
            'totalResults': len(formatted_videos)
        }
    except Exception as e:
        logger.exception(f"Error in get_trending_videos: {e}")
        return {'error': str(e)}

@mcp.tool(
    name="get_video_enhanced_transcript",
    description="Advanced transcript extraction tool with filtering, search, and multi-video capabilities. Provides rich transcript data for detailed analysis and processing. Features: 1) Extract transcripts from multiple videos; 2) Filter by time ranges; 3) Search within transcripts; 4) Segment transcripts; 5) Format output in different ways; 6) Include video metadata.",
)
async def get_video_enhanced_transcript(
    video_ids: List[str],
    language: Optional[str] = 'ko',
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    query: Optional[str] = None,
    case_sensitive: Optional[bool] = False,
    segment_method: Optional[str] = "equal",
    segment_count: Optional[int] = 2,
    format: Optional[str] = "timestamped",
    include_metadata: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Get enhanced transcript for one or more YouTube videos with advanced filtering and processing
    
    Args:
        video_ids (List[str]): List of YouTube video IDs (max 5)
        language (str, optional): Language code for transcript
        start_time (int, optional): Start time in seconds
        end_time (int, optional): End time in seconds
        query (str, optional): Search query
        case_sensitive (bool, optional): Whether to use case-sensitive search
        segment_method (str, optional): Segment method ("equal" or "smart")
        segment_count (int, optional): Number of segments
        format (str, optional): Output format ("raw", "timestamped", "merged")
        include_metadata (bool, optional): Whether to include video details
    
    Returns:
        Dict[str, Any]: Enhanced transcript data
    """
    try:
        # Validate input
        if not video_ids:
            return {'error': "No video IDs provided"}
        
        if len(video_ids) > 5:
            return {'error': "Maximum 5 video IDs allowed"}
            
        # Build options from individual parameters
        options = {
            'language': language,
            'format': format,
            'includeMetadata': include_metadata
        }
        
        # Add time range filter if specified
        if start_time is not None or end_time is not None:
            options['timeRange'] = {
                'start': start_time,
                'end': end_time
            }
            
        # Add search filter if specified
        if query:
            options['search'] = {
                'query': query,
                'caseSensitive': case_sensitive,
                'contextLines': 2  # Default context lines
            }
            
        # Add segment option if specified
        options['segment'] = {
            'method': segment_method,
            'count': segment_count
        }
        
        # Call the enhanced transcript method
        transcript = youtube_service.get_video_enhanced_transcript(video_ids, options)
        
        return transcript
    except Exception as e:
        logger.exception(f"Error in get_video_enhanced_transcript: {e}")
        return {'error': str(e)}

# Server start point
if __name__ == "__main__":
    logger.info("Starting YouTube MCP server...")
    try:
        mcp.run()
    except Exception as e:
        logger.exception(f"Error running MCP server: {e}")
