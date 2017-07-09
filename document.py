#!/usr/bin/env python3
import textutil, source
from json import JSONEncoder

class DocumentEncoder(JSONEncoder):
    def default(self, document):
        if isinstance(document, Document):
            return {'interesting': document.interesting, 'data': document.data}
        else:
            return json.JSONEncoder.default(self, document)

class Document():
    def __init__(self, data, interesting = None):
        self.data = data
        self.interesting = interesting
        self.predicted_interesting = None
        self.score = None
        self._new = True

    @property
    def id(self):
        return self.data['id']

    @property
    def url(self):
        pass

    @property
    def title(self):
        pass

    @property
    def text(self):
        pass

    @property
    def user(self):
        pass

    @property
    def image_url(self):
        pass

    @property
    def classification_text(self):
        text_items = filter(None, self.classification_text_items)
        text = ' '.join(list(map(textutil.normalized_text, text_items)))
        return text

    @property
    def classification_text_items(self):
        return []

    @property
    def source(self):
        return source.name_from_module(self.__module__)

    def __repr__(self):
        return '{}.{}({}, interesting={})'.format(self.__module__, self.__class__.__name__, self.data, self.interesting)

    @property
    def new(self):
        current = self._new
        self._new = False
        return current
