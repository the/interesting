#!/usr/bin/env python3
import document, html

class Document(document.Document):
    @property
    def url(self):
        user = self.data['user']
        return 'https://twitter.com/{}/status/{}'.format(user['screen_name'], self.id)

    @property
    def title(self):
        if self.children and not self.__is_quote:
            return 'RT'

        text = self.data['text']
        return html.unescape(text)

    @property
    def user(self):
        user = self.data['user']
        return '{} @{}'.format(user['name'], user['screen_name'])

    @property
    def image_url(self):
        user = self.data['user']
        return user['profile_image_url']

    @property
    def classification_text_items(self):
        # return [self.data['user']['screen_name'], self.data['text']]
        # TODO: remove URLs, @-naming etc.?
        text_items = []

        if self.children:
            if self.__is_quote:
                text_items.append(self.title)
            for child in self.children:
                text_items.append(child.title)
        else:
            text_items.append(self.title)

        return text_items

    @property
    def children(self):
        children = []

        if 'retweeted_status' in self.data:
            children.append(Document(self.data['retweeted_status']))
        if 'quoted_status' in self.data:
            children.append(Document(self.data['quoted_status']))

        return children

    @property
    def __is_quote(self):
        return 'quoted_status' in self.data and not 'retweeted_status' in self.data
