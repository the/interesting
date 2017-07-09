#!/usr/bin/env python3
import feedparser, time, logging
from threading import Thread
from source.theverge.document import Document
from source import get_logger

DEFAULT_CONFIG = {
    'delay': 2,
    'interval': 60
}

logger = get_logger(__name__)

def get_articles():
    articles = []

    feed = feedparser.parse('https://www.theverge.com/rss/index.xml')
    if feed:
        for entry in feed.entries:
            doc = Document({
                'id': entry.id,
                'url': entry.link,
                'title': entry.title,
                'author': entry.author,
                'published': entry.published
            })
            articles.append(doc)

    return articles

class Bot(Thread):
    def __init__(self, queue, config):
        super(Bot, self).__init__()
        self.daemon = True
        self.queue = queue
        self.config = {**DEFAULT_CONFIG, **config}
        self.articles = {}

    def remember_article(self, article):
        self.articles[article.id] = article

    def run(self):
        time.sleep(self.config['delay'])

        while True:
            logger.info('Collecting articles')

            new_article_count = 0
            for article in get_articles():
                if article.id not in self.articles:
                    logger.debug('New article {}'.format(article))
                    self.queue.put(article)
                    self.remember_article(article)
                    new_article_count = new_article_count + 1

            if new_article_count > 0:
                logger.info('New {}'.format(new_article_count))

            time.sleep(self.config['interval'])
