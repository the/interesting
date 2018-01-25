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
        return 'https://cdn0.vox-cdn.com/images/verge/2.0/verge-icon-196x196.v503bbf1.png'

    @property
    def classification_text_items(self):
        return [self.data['title']]
