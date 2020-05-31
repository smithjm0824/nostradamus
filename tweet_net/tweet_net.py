import configparser
import tweepy
import pika

# Import Twitter API Keys from Config file
config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['KEYS']['api_key']
consumer_secret = config['KEYS']['api_secret']
access_token = config['TOKENS']['access_token']
access_token_secret = config['TOKENS']['access_token_secret']

# Instantiate Tweepy Client
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="tweets")


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if hasattr(status, "retweeted_status"):
            return

        if hasattr(status, 'extended_tweet'):
            data = status.extended_tweet['full_text']
        else:
            data = status.text

        channel.basic_publish(exchange='',
                              routing_key='tweets',
                              body=data)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode="extended")
stream.filter(track=["Trump"])

