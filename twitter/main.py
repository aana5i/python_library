import tweepy
from config.config import get_credentials
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = get_credentials()
# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY,
                           CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,
                      ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

author = ["InfiniteFleet", "Sonny_AD", "Excellion", "infinitefleetfr"]
tweets = api.home_timeline(count=10)
for tweet in tweets:
    if tweet.author.screen_name in author:
        if not tweet.favorited:
            # Mark it as Liked, since its not done it yet
            try:
                tweet.favorite()
                print(f"Liking tweet {tweet.text} of {tweet.author.screen_name}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)

