import socket
import sys
import requests
import requests_oauthlib
import json
from kafka import SimpleProducer, KafkaClient
import time


# My Own Access Credentials
ACCESS_TOKEN = 'YOURACCESSTOKEN'
ACCESS_SECRET = 'YOURACCESSSECRET'
CONSUMER_KEY = 'YOURCONSUMERKEY'
CONSUMER_SECRET = 'YOURCONSUMERSECRET'

my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# Set Kafka Producer
twitter_topic="topic_twitter"
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)


def get_tweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    query_data = [('language', 'es'), ('locations', '-3.7834,40.3735, -3.6233, 40.4702'),('track','Madrid')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response

def send_tweets_to_kafka(http_resp):
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text']
            print("Tweet Text: " + tweet_text)
            print ("------------------------------------------")
            tweet_data = bytes(tweet_text + '\n', 'utf-8')
            producer.send_messages(twitter_topic, tweet_data)
        except:
            print("Error received during Kafka step!")
            e = sys.exc_info()[0]
            print("Error: %s" % e)


def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text']
            print("Tweet Text: " + tweet_text)
            print ("------------------------------------------")
        except Exception as e:
            print("Error received during Spark step!")
            e1 = sys.exc_info()[0]
            print("Error e: %s" % str(e))
            print("Error e1: %s" % str(e1))

resp = get_tweets()
send_tweets_to_kafka(resp)