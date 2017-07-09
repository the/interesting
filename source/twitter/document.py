#!/usr/bin/env python3
import document, html

class Document(document.Document):
    @property
    def url(self):
        user = self.data['user']
        return 'https://twitter.com/{}/status/{}'.format(user['screen_name'], self.id)

    @property
    def title(self):
        text = self.data['text']
        if 'retweeted_status' in self.data:
            text = self.data['retweeted_status']['text']

        return html.unescape(text)

    @property
    def user(self):
        user = self.__tweet_user
        return '{} @{}'.format(user['name'], user['screen_name'])

    @property
    def image_url(self):
        user = self.__tweet_user
        return user['profile_image_url']

    @property
    def classification_text_items(self):
        # return [self.data['user']['screen_name'], self.data['text']]
        # TODO: remove URLs, @-naming etc.?
        return [self.title]

    @property
    def __tweet_user(self):
        user = self.data['user']
        if 'retweeted_status' in self.data:
            user = self.data['retweeted_status']['user']

        return user
