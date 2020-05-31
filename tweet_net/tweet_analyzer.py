import pika
from textblob import TextBlob

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="tweets")


def callback(ch, method, properties, body):

    blob = TextBlob(str(body))
    print("[X] Received %r" % body)
    print("[Score] : " + str(blob.sentiment[0]) + ", " + str(blob.sentiment[1]))


channel.basic_consume(queue='tweets',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()