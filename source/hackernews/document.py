#!/usr/bin/env python3
import document

class Document(document.Document):
    @property
    def url(self):
        return 'https://news.ycombinator.com/item?id={}'.format(self.id)

    @property
    def title(self):
        return self.data['title']

    @property
    def user(self):
        return self.data['submitter']

    @property
    def image_url(self):
        return 'http://www.ycombinator.com/images/ycombinator-logo-fb889e2e.png'

    @property
    def classification_text_items(self):
        return [self.data['submitter'], self.data['title']]
