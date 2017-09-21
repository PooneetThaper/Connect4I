import numpy as np

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
        move.append(float(line[moveLocation])/10)

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

for k in range(len(boards)):
    print boards[k],move[k]

X = np.array(boards)
y = np.array(move)

syn=[]

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
        while g<(n+2):
            l.append(nonlin(np.dot(l[g-1], syn[g-1])))
            g+=1

        # Back propagation of errors using the chain rule.
        errors = []
        deltas = []

        #Top level error and delta
        top_error = y - l[n+1]
        errors.append(top_error)
        top_delta = top_error*nonlin(l[n+1],deriv=True)
        deltas.append(top_error)
        #Deeper level error and delta
        l4_error = y - l[4]
        l4_delta = l4_error*nonlin(l[4],deriv=True)
        print l4_delta
        print syn[3]
        l3_error = l4_delta.dot(syn[3].T)
        l3_delta = l3_error*nonlin(l[3],deriv=True)
        l2_error = l3_delta.dot(syn[2].T)
        l2_delta = l2_error*nonlin(l[2], deriv=True)
        l1_error = l2_delta.dot(syn[1].T)
        l1_delta = l1_error * nonlin(l[1],deriv=True)

        #for k in range(n):
        #    e=deltas[k].dot(syn[n-k].T)
        #    errors.append(e)
        #    d=e*nonlin(l[n-k],deriv=True)
        #    deltas.append(d)

        if(j % 100) == 0:   # Only print the error every 10000 steps, to save time and limit the amount of output.
            print j,":Error: ",str(np.mean(np.abs(top_error)))

        #update weights (no learning rate term)
        syn[3] += l[3].T.dot(l4_delta)/2
        syn[2] += l[2].T.dot(l3_delta)/2
        syn[1] += l[1].T.dot(l2_delta)/2
        syn[0] += l[0].T.dot(l1_delta)/2

        #for k in range(n+1):
        #    syn[k] += np.transpose(l[k]).dot(deltas[n-k])/5


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
    numOutputs=1
    n=3
    k=9
    #print(X)
    #print(y)
    build(numInputs,numOutputs,n,k)
    train(n,100000)
    test(n)

main()
