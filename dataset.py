#!/usr/bin/env python3
import os, json, importlib
from document import Document, DocumentEncoder

class DataSet:
    def __init__(self, source):
        self.data = {}
        self.source = source
        self.doclib = importlib.import_module('source.{}.document'.format(source))
        self.load()

    @property
    def all_documents(self):
        return sorted(self.data.values(), key=lambda doc: doc.id)

    def update_document(self, doc):
        self.data[doc.id] = doc

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                items = json.load(file)
                for item in items:
                    doc = self.doclib.Document(item['data'], item['interesting'])
                    self.data[doc.id] = doc

    def save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w') as file:
            json.dump(self.all_documents, file, indent=4, cls=DocumentEncoder)

    @property
    def filename(self):
        return os.path.join('dataset', '{}.json'.format(self.source))
