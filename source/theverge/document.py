#!/usr/bin/env python3
import document

class Document(document.Document):
    @property
    def url(self):
        return self.data['url']

    @property
    def title(self):
        return self.data['title']

    @property
    def user(self):
        return self.data['author']

    @property
    def image_url(self):
        return 'https://cdn.freebiesupply.com/images/large/2x/the-verge-logo-transparent.png'

    @property
    def classification_text_items(self):
        return [self.data['title']]
