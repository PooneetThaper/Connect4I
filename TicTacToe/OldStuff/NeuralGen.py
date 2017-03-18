'''
This code aims to create a regression model using an artificial neural network
and gradient descent. However, for this particular problem and considering the
dataset, a classification approach would be better. This code will be retired
to the OldStuff folder and replaced by an SciKit learn
'''

import numpy as np

boards= []
expectedOutput= []
bestMoves = []

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

        b = []
        for k in range(9):
            b.append(0)
        location = 8
        while boardCode > 0:
            n = int(boardCode/3)
            b[location]= float( boardCode - 3*n )
            boardCode = n
            location = location - 1
        for k in range(9):
            b[k] = b[k] -1
        boards.append(b)

        bestMoves.append(int(line[moveLocation]))

        g = []
        for k in range(9):
            g.append(float(0))
        g[int(line[moveLocation])] = (float(1))
        expectedOutput.append(g)


for k in range(len(boards)):
    print boards[k],expectedOutput[k]

X = np.array(boards)
y = np.array(expectedOutput)

syn=[]

def softmax(x, deriv=False):
    if deriv==False:
        retval = []
        for k in x:
            n = []
            m = []
            sum=0
            for j in k:
                n.append(np.exp(j))
            for j in n:
                sum = sum + j
            print sum
            for j in n:
                m.append(j/sum)
            k=m
        print x
        return x
    else:
        return x*(1-x)

def nonlin(x, deriv=False):
    g = np.exp(-x)
    if(deriv==True):
        return (x*(1-x))
    return 1/(1+g)

def train(n,iter_n):
    for j in range(iter_n):
        l=[]
        l.append(X)
        g=1
        while g<(n+1):
            l.append(nonlin(np.dot(l[g-1], syn[g-1])))
            g+=1

        l.append(softmax(np.dot(l[g-1], syn[g-1])))
        print l[n+1]
        # Back propagation of errors using the chain rule.
        errors = []
        deltas = []

        #Top level error and delta
        top_error = y - l[n+1]
        errors.append(top_error)
        top_delta = top_error*softmax(l[n+1],deriv=True)
        deltas.append(top_error)
        #Deeper level error and delta
        for k in range(n):
            e=deltas[k].dot(syn[n-k].T)
            errors.append(e)
            d=e*nonlin(l[n-k],deriv=True)
            deltas.append(d)

        if(j % 1) == 0:   # Only print the error every 10000 steps, to save time and limit the amount of output.
            print j,":Error: ",str(np.mean(np.abs(top_error)))

        #update weights (no learning rate term)
        for k in range(n+1):
            syn[k] += np.transpose(l[k]).dot(deltas[n-k])/5


def build(numIn,numOut,numHiddenLayers,numNeuronsHidden):
    last=numIn
    np.random.seed(1)
    for i in range(numHiddenLayers):
        syn.append(2*np.random.random((last,numNeuronsHidden))-1)
        last = numNeuronsHidden
    syn.append(2*np.random.random((last,numOut))-1)

def test(n):
    l=[]
    l.append(X)
    g=1
    while g<(n+2):
        l.append(nonlin(np.dot(l[g-1], syn[g-1])))
        g+=1
    print(l[n+1])

def main():
    numInputs=9
    numOutputs=9
    n=5
    k=20
    #print(X)
    #print(y)
    build(numInputs,numOutputs,n,k)
    train(n,100000)
    test(n)

main()
