#!/usr/bin/env python3
import webutil, time, logging
from threading import Thread
from source.hackernews.document import Document
from source import get_logger

DEFAULT_CONFIG = {
    'delay': 2,
    'interval': 60,
    'pages': 3
}

logger = get_logger(__name__)

def get_stories(pages):
    stories = []
    for page in range(1, pages + 1):
        stories.extend(get_stories_of_page(page))

    return reversed(stories)

def get_stories_of_page(page):
    stories = []
    page = webutil.get_page('https://news.ycombinator.com/news?p={}'.format(page))

    if page:
        for story in page.find_all('tr', class_='athing'):
            story_id = int(story.attrs['id'])
            story_link = story.find('a', class_='titlelink')
            url = story_link.attrs['href']
            title = story_link.text
            hnuser = story.next_sibling.find('a', class_='hnuser')
            submitter = hnuser.text if hnuser else None
            doc = Document({
                'id': story_id,
                'url': url,
                'title': title,
                'submitter': submitter,
                'timestamp': time.time()
            })
            stories.append(doc)

    return stories

class Bot(Thread):
    def __init__(self, queue, config):
        super(Bot, self).__init__()
        self.daemon = True
        self.queue = queue
        self.config = {**DEFAULT_CONFIG, **config}
        self.stories = {}

    def remember_story(self, story):
        self.stories[story.id] = story

    def run(self):
        time.sleep(self.config['delay'])

        while True:
            try:
                logger.info('Collecting stories')

                new_story_count = 0
                for story in get_stories(self.config['pages']):
                    if story.id not in self.stories:
                        logger.debug('New story {}'.format(story))
                        self.queue.put(story)
                        self.remember_story(story)
                        new_story_count = new_story_count + 1

                if new_story_count > 0:
                    logger.info('New {}'.format(new_story_count))
            except Exception as err:
                logger.error('error: {}'.format(err))

            time.sleep(self.config['interval'])
