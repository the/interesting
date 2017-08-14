#!/usr/bin/env python3
import importlib, yaml, logging
from gevent.wsgi import WSGIServer
from flask import Flask, render_template, jsonify, request
from queue import Queue
from dataset import DataSet
from classifier import Classifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

queue = Queue()
docs = []
classifiers = {}

sources_config = yaml.safe_load(open('config.yml', 'r'))
for source, config in sources_config['source'].items():
    logger.info('Starting source {}'.format(source))
    lib = importlib.import_module('source.{}.bot'.format(source))
    bot = lib.Bot(queue, config)
    bot.start()

    dataset = DataSet(source)
    classifiers[source] = Classifier(dataset.all_documents)

def update_docs():
    while not queue.empty():
        doc = queue.get()
        doc.predicted_interesting = classifiers[doc.source].predict(doc)
        docs.insert(0, doc)

application = Flask(__name__)
application.config['TEMPLATES_AUTO_RELOAD'] = True

@application.route('/')
def home():
    update_docs()
    filtered = [doc for doc in docs if doc.interesting or (doc.predicted_interesting and doc.interesting == None)]
    return render_template('documents.html', docs=filtered, title='interesting', sources=classifiers.keys(), selected='interesting')

@application.route('/source/<source>')
def source(source):
    update_docs()
    filtered = [doc for doc in docs if doc.source == source]
    return render_template('documents.html', docs=filtered, title=source, sources=classifiers.keys(), selected=source)

@application.route('/interesting/<source>', methods=['POST'])
def interesting(source):
    interesting = request.form['interesting'] == 'yes'
    doc_id = request.form['id']
    dataset = DataSet(source)
    for doc in docs:
        if str(doc.id) == doc_id:
            logger.info('Saving: ' + doc_id)
            doc.interesting = interesting
            dataset.update_document(doc)
            dataset.save()
            classifiers[source] = Classifier(dataset.all_documents)
            break
    return '{} -- {} -- {}'.format(source, doc_id, interesting)

http_server = WSGIServer(('127.0.0.1', 5000), application)
http_server.serve_forever()
