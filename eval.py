#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splrep, splev
from dataset import DataSet
from classifier import Classifier

if len(sys.argv) < 2:
    print('Usage: eval.py source')
    sys.exit(-1)

source = sys.argv[1]

def plot_eval(ax, classifier_scores, x):
    for name, scores in classifier_scores.items():
        # line smoothing from https://stackoverflow.com/a/30437051/3782059
        tck = splrep(x, scores)
        xnew = np.linspace(x[0], x[-1])
        ynew = splev(xnew, tck)
        ax.plot(xnew, ynew, label=name, alpha=0.5)

    ax.legend(loc='lower right')
    ax.axis(xmin=x[0], xmax=x[-1], ymin=0, ymax=1)
    ax.grid()

dataset = DataSet(source)
classifier = Classifier(dataset.all_documents)
evaluation = classifier.eval()

for name, scores in evaluation['scores'].items():
    print('average score {}: {}'.format(name, np.mean(scores)))

fig, axes = plt.subplots(nrows=2, ncols=1)

plt.suptitle(source)
plot_eval(axes[0], evaluation['scores'], evaluation['scores_x'])
plot_eval(axes[1], evaluation['test_scores'], evaluation['test_scores_x'])

plt.show()
