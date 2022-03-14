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
        return 'https://upload.wikimedia.org/wikipedia/commons/d/d5/Y_Combinator_Logo_400.gif'

    @property
    def classification_text_items(self):
        return [self.data['submitter'], self.data['title']]
