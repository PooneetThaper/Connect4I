from sklearn import svm
from sklearn.externals import joblib

boards= []
move= []

with open('OutputFiles/bestMoves.txt','r') as f:
    for line in f:
        #print line
        b = []
        moveLocation = 0
        for char in line:
            moveLocation = moveLocation + 1
            if char != ':':
                b.append(char)
            else:
                break
        boardCode = int(''.join(b))
        move.append(int(line[moveLocation]))

        b = []
        for k in range(9):
            b.append(0)
        location = 8
        while boardCode > 0:
            n = int(boardCode/3)
            b[location]= ( boardCode - 3*n )
            boardCode = n
            location = location - 1
        for k in range(9):
            b[k] = b[k] -1
        boards.append(b)

'''
for k in range(len(boards)):
    print boards[k],move[k]
'''

clf = svm.SVC()
clf = clf.fit(boards,move)
print (clf.predict([1,1,0,-1,-1,0,0,0,0]))

joblib.dump(clf, 'SVM.pkl')
