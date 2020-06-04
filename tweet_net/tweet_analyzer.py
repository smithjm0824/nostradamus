import pika
from textblob import TextBlob
import pymongo
import datetime
from datetime import timezone

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="tweets")

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
tweet_db = mongo_client['tweet-sentiment']
tweet_collection = tweet_db['records']


def callback(ch, method, properties, body):

    blob = TextBlob(str(body))
    utc_timestamp = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
    print("[X] Received %r" % body)
    polarity, subjectivity = blob.sentiment
    if polarity != 0.0 or subjectivity != 0.0:
        _id = tweet_collection.insert_one({'utc_timestamp' : utc_timestamp,
                                           'polarity' : blob.sentiment[0],
                                           'subjectivity' : blob.sentiment[1]})
        print("Saving analysis")


channel.basic_consume(queue='tweets',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()