#!/usr/bin/env python3
import tweepy, time
from threading import Thread
from source.twitter.document import Document
from source import get_logger

logger = get_logger(__name__)

class Bot(Thread):
    def __init__(self, queue, config):
        super(Bot, self).__init__()
        self.daemon = True
        self.queue = queue
        self.config = config
        self.tweets = {}

    def remember_status(self, status):
        self.tweets[status.id] = status

    def run(self):
        auth = tweepy.OAuthHandler(self.config['consumer_key'], self.config['consumer_secret'])
        auth.set_access_token(self.config['access_token'], self.config['access_token_secret'])

        bot = self

        class TweetListener(tweepy.StreamListener):
            def on_status(self, status):
                doc = Document(status._json)
                logger.info('Received status with id={}'.format(status.id))
                bot.remember_status(doc)
                bot.queue.put(doc)

            def on_error(self, status_code):
                if status_code == 420:
                    logger.error('Twitter stream error: RATE LIMITED')
                else:
                    logger.error('Twitter stream error: {}'.format(status_code))

        while True:
            try:
                logger.info('Start Twitter timeline streaming')
                listener = TweetListener()
                stream = tweepy.Stream(auth, listener)
                stream.userstream()
            except Exception as err:
                logger.error('Twitter stream broken: {}'.format(err))
                time.sleep(10)
