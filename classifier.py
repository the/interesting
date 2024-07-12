#!/usr/bin/env python3
import logging
import numpy as np
from collections import defaultdict
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import cross_validate

logger = logging.getLogger(__name__)

class Classifier:
    def __init__(self, docs):
        self.X = []
        self.y = []
        for doc in docs:
            self.X.append(doc.classification_text)
            self.y.append(doc.interesting)

        if True in self.y and False in self.y:
            self.pipeline = self.pipelines['SGDClassifier.log']
            self.pipeline.fit(self.X, self.y)

    def predict(self, doc):
        try:
            classifier = self.pipeline.named_steps['classifier']
            if hasattr(classifier, 'predict_proba'):
                # example: [(False, 0.70580146379303743), (True, 0.29419853620696201)]
                probabilities = zip(self.pipeline.classes_, self.pipeline.predict_proba([doc.classification_text])[0])
                interesting_probability = [p[1] for p in probabilities if p[0] == True][0]
                doc.score = interesting_probability

            return self.pipeline.predict([doc.classification_text])[0]
        except AttributeError as e:
            logger.error(e)
            return False

    def eval(self):
        CV = 3
        scores = defaultdict(dict)

        for name, pipeline in self.pipelines.items():
            cv_results = cross_validate(pipeline, self.X, self.y, cv=CV, scoring=('accuracy', 'precision', 'recall', 'f1'))
            scores[name] = {
                'accuracy': cv_results['test_accuracy'],
                'precision': cv_results['test_precision'],
                'recall': cv_results['test_recall'],
                'f1': cv_results['test_f1']
            }

        return dict(scores)

    @property
    def pipelines(self):
        return {
            'MultinomialNB': Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', MultinomialNB(alpha=1))
            ]),
            'BernoulliNB': Pipeline([
                ('vectorizer', CountVectorizer()),
                ('classifier', BernoulliNB(binarize=0.0))
            ]),
            'LogisticRegression': Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', LogisticRegression())
            ]),
            'LinearSVC': Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', LinearSVC())
            ]),
            'SVC.linear': Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', SVC(kernel='linear', probability=True))
            ]),
            'SGDClassifier.hinge': Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', SGDClassifier(loss='hinge', max_iter=100))
            ]),
            'SGDClassifier.log': Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', SGDClassifier(loss='log_loss', max_iter=100))
            ]),
            'RandomForest': Pipeline([
                ('vectorizer',  TfidfVectorizer()),
                ('classifier', RandomForestClassifier(random_state=0))
            ]),
        }
