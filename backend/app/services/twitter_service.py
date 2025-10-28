import tweepy
from app.schemas.comment import Comment
from app.utils.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TwitterService:
    def __init__(self):
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Twitter API v2 client"""
        try:
            client = tweepy.Client(
                bearer_token=settings.TWITTER_BEARER_TOKEN,
                consumer_key=settings.TWITTER_API_KEY,
                consumer_secret=settings.TWITTER_API_SECRET,
                access_token=settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=settings.TWITTER_ACCESS_SECRET,
                wait_on_rate_limit=True
            )
            logger.info("Twitter client initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Error initializing Twitter client: {e}")
            raise
    
    async def get_tweets_by_keyword(self, keyword: str, max_results: int = 100) -> list[Comment]:
        """Fetch tweets by keyword using Twitter API v2"""
        try:
            tweets = self.client.search_recent_tweets(
                query=keyword,
                max_results=min(max_results, 100),
                tweet_fields=['created_at', 'author_id', 'text']
            )
            
            comments = []
            if tweets.data:
                for tweet in tweets.data:
                    comment = Comment(
                        id=str(tweet.id),
                        text=tweet.text,
                        author=str(tweet.author_id),
                        timestamp=tweet.created_at,
                        platform="twitter"
                    )
                    comments.append(comment)
            
            logger.info(f"Fetched {len(comments)} tweets for keyword: {keyword}")
            return comments
        except Exception as e:
            logger.error(f"Error fetching tweets: {e}")
            raise
    
    async def get_user_tweets(self, username: str, max_results: int = 100) -> list[Comment]:
        """Fetch tweets from a specific user"""
        try:
            user = self.client.get_user(username=username)
            if not user.data:
                return []
            
            tweets = self.client.get_users_tweets(
                id=user.data.id,
                max_results=min(max_results, 100),
                tweet_fields=['created_at', 'author_id', 'text']
            )
            
            comments = []
            if tweets.data:
                for tweet in tweets.data:
                    comment = Comment(
                        id=str(tweet.id),
                        text=tweet.text,
                        author=username,
                        timestamp=tweet.created_at,
                        platform="twitter"
                    )
                    comments.append(comment)
            
            logger.info(f"Fetched {len(comments)} tweets for user: {username}")
            return comments
        except Exception as e:
            logger.error(f"Error fetching user tweets: {e}")
            raise

# Singleton instance
_twitter_service = None

def get_twitter_service() -> TwitterService:
    global _twitter_service
    if _twitter_service is None:
        _twitter_service = TwitterService()
    return _twitter_service
