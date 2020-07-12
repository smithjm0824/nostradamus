import configparser
import tweepy
import botometer
from textblob import TextBlob
import redis
import time
from domain.Users import User, Users
from domain.Tweets import Tweet

config = configparser.ConfigParser()
config.read('../config.ini')

app_key = config['RAPIDAPI']['api_key']
consumer_key = config['KEYS']['api_key']
consumer_secret = config['KEYS']['api_secret']
access_token = config['TOKENS']['access_token']
access_token_secret = config['TOKENS']['access_token_secret']

twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret
}

redis_client = redis.Redis(host="localhost", port=6379, db=0)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=app_key,
                          **twitter_app_auth)

users = Users()
processed_users = Users()


def bot_or_not():
    print(len(users), len(processed_users))
    if len(users) > 0:
        user_ids = users.get_user_ids()
        for id_str, result in bom.check_accounts_in(user_ids):
            tmp_usr = users.get(id_str)
            tmp_usr.assign(result['cap']['english'])
            processed_users.add(tmp_usr)
        print(str(len(user_ids)) + " users processed.")
        users.delete(user_ids)


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if hasattr(status, "retweeted_status"):
            return

        if hasattr(status, 'extended_tweet'):
            data = status.extended_tweet['full_text']
        else:
            data = status.text

        key = status.id_str
        user_id = status.user.id_str

        cache_tweet = {
            'user_id': user_id,
            'utc_created_at': status.created_at.strftime("%m-%d-%Y, %H:%M:%S"),
            'tweet_body': data
        }

        blob = TextBlob(data)
        polarity, subjectivity = blob.sentiment
        utc_created_at = status.created_at.strftime("%m-%d-%Y, %H:%M:%S")

        tweet = Tweet(tweet_id=key, author_id=user_id, polarity=polarity, subjectivity=subjectivity,
                      created_timstm=utc_created_at, tweet_body=data)

        if redis_client.hgetall(key):
            print("Key Exists")

        redis_client.hmset(key, cache_tweet)

        user = User(user_id)
        user.add(tweet)
        users.add(user)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode="extended")
stream.filter(track=["$FB", "$TSLA", "$AAPL", "$GM", "$BTC"], is_async=True)

while True:
    time.sleep(5)
    bot_or_not()
