#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt
from dataset import DataSet
from classifier import Classifier

if len(sys.argv) < 2:
    print('Usage: eval.py source')
    sys.exit(-1)

source = sys.argv[1]

dataset = DataSet(source)
documents = dataset.all_documents
classifier = Classifier(documents)
evaluation = classifier.eval()

fig, ax = plt.subplots()
plt.suptitle(source)
ax.axis(xmin=-0.05, xmax=1.05, ymin=-0.05, ymax=1.05)
ax.set_xlabel('recall')
ax.set_ylabel('precision')
ax.grid()

linesep = '-' * 50

print(linesep)
print('number of documents: {}'.format(len(documents)))
print(linesep)

for name, scores in evaluation.items():
    for scoring, values in scores.items():
        print('{:20} {:10}: {:5.3f} (std={:5.3f})'.format(name, scoring, np.mean(values), np.std(values)))
    print(linesep)

    x = scores['recall']
    y = scores['precision']
    ax.plot(x, y, 'o', label=name, alpha=0.5)

ax.legend(loc='lower right')
plt.show()
