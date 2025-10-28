from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.schemas.comment import Comment
from app.utils.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.youtube = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize YouTube API client"""
        try:
            youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
            logger.info("YouTube client initialized successfully")
            return youtube
        except Exception as e:
            logger.error(f"Error initializing YouTube client: {e}")
            raise
    
    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return url  # Assume it's already a video ID
    
    async def get_video_comments(self, video_url: str, max_results: int = 100) -> list[Comment]:
        """Fetch comments from a YouTube video"""
        try:
            video_id = self._extract_video_id(video_url)
            comments = []
            next_page_token = None
            
            while len(comments) < max_results:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments)),
                    pageToken=next_page_token,
                    order="time",
                    textFormat="plainText"
                )
                
                response = request.execute()
                
                for item in response['items']:
                    snippet = item['snippet']['topLevelComment']['snippet']
                    comment = Comment(
                        id=item['id'],
                        text=snippet['textDisplay'],
                        author=snippet['authorDisplayName'],
                        timestamp=datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')),
                        platform="youtube"
                    )
                    comments.append(comment)
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            logger.info(f"Fetched {len(comments)} comments for video: {video_id}")
            return comments
        except HttpError as e:
            logger.error(f"HTTP Error fetching YouTube comments: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching YouTube comments: {e}")
            raise
    
    async def get_channel_comments(self, channel_id: str, max_results: int = 100) -> list[Comment]:
        """Fetch comments from all videos in a channel"""
        try:
            # Get channel's videos
            request = self.youtube.search().list(
                part="id",
                channelId=channel_id,
                maxResults=10,
                order="date",
                type="video"
            )
            response = request.execute()
            
            all_comments = []
            for item in response['items']:
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                comments = await self.get_video_comments(video_url, max_results // 10)
                all_comments.extend(comments)
                
                if len(all_comments) >= max_results:
                    break
            
            logger.info(f"Fetched {len(all_comments)} comments for channel: {channel_id}")
            return all_comments[:max_results]
        except Exception as e:
            logger.error(f"Error fetching channel comments: {e}")
            raise

# Singleton instance
_youtube_service = None

def get_youtube_service() -> YouTubeService:
    global _youtube_service
    if _youtube_service is None:
        _youtube_service = YouTubeService()
    return _youtube_service
