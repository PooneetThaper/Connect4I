import numpy as np

def nonlin(x, deriv=False):
    if(deriv==True):
        return (x*(1-x))
    return 1/(1+np.exp(-x))


board = [  [ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0],
                    [-1, 1,-1,-1, 1, 1, 1],
                    [ 1, 1, 1,-1, 1,-1,-1],
                    [ 1, 1,-1,-1, 1, 1, 1]]

players=[]


def runPlayer(playerNum):
    b=[]
    for row in board:
        for k in row:
            b.append(k)
    out=(nonlin(np.dot(b, players[playerNum])))
    m=out[0]
    index=0
    for x in range(1,7):
        if(out[x]>m):
            m=out[x]
            index=x
    return index

def start():
    numIn=42
    numOut=7
    numPlayers=8
    np.random.seed(0)
    for k in range(numPlayers):
        players.append(2*np.random.random((numIn,numOut))-1)
    print(runPlayer(4))

if __name__ == '__main__':
    start()
