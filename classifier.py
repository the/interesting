#!/usr/bin/env python3
import textutil
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split

class Classifier:
    def __init__(self, docs):
        self.X = []
        self.y = []
        for doc in docs:
            self.X.append(doc.classification_text)
            self.y.append(doc.interesting)

        if True in self.y and False in self.y:
            self.pipeline = self.pipelines['MultinomialNB']
            self.pipeline.fit(self.X, self.y)

    def predict(self, doc):
        try:
            # example: [(False, 0.70580146379303743), (True, 0.29419853620696201)]
            probabilities = zip(self.pipeline.classes_, self.pipeline.predict_proba([doc.classification_text])[0])
            interesting_probability = [p[1] for p in probabilities if p[0] == True][0]
            doc.score = interesting_probability
            return self.pipeline.predict([doc.classification_text])[0]
        except AttributeError:
            return False

    def eval(self):
        CV = 10
        scores = {}

        train_sizes = np.linspace(0.05, 0.8, 16)
        test_scores = {}
        test_scores_x = []

        for name, pipeline in self.pipelines.items():
            scores[name] = cross_val_score(pipeline, self.X, self.y, cv=CV).tolist()

        for train_size in train_sizes:
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, train_size=train_size, random_state=0)
            test_scores_x.append(len(X_train))

            for name, pipeline in self.pipelines.items():
                if name not in test_scores:
                    test_scores[name] = []

                pipeline.fit(X_train, y_train)
                test_scores[name].append(pipeline.score(X_test, y_test))

        return {
            'documents': len(self.X),
            'scores': scores,
            'scores_x': np.arange(CV),
            'test_scores': test_scores,
            'test_scores_x': test_scores_x,
        }

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
            'RandomForest': Pipeline([
                ('vectorizer',  TfidfVectorizer()),
                ('classifier', RandomForestClassifier(random_state=0))
            ]),
        }
