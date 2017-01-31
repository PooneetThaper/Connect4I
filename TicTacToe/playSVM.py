from sklearn import svm
from sklearn.externals import joblib
import numpy as np
import sys

board = []
clf = joblib.load('SVM.pkl')

input = sys.argv[1]

for i in input:
    board.append(int(i)-1)

b = np.array(board)

print clf.predict(b)[0]
