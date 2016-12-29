import numpy as np
import csv
import time

def nonlin(x, deriv=False):
    if(deriv==True):
        return (x*(1-x))
    return 1/(1+np.exp(-x))


board = []
colTracker = []
players=[]

def addPiece(column, p):
	count=0
	winner=0
	if(colTracker[column]<0): # LOSE CONDITION MET
		winner=p*-1
		#print winner
		return winner
	else: # ADD PIECE TO COLUMN
		board[colTracker[column]][column]=p

		for j in range(0, 7): # check row win
			if((count > 0) and (board[colTracker[column]][j] != p)): # reset counter if not consecutive
				count = 0
			if(board[colTracker[column]][j] == p):
				count += 1

				if(count == 4): # WIN CONDITION MET
					winner = p
					return winner
		count = 0 # reset

		# check diagonal win
		# diagonal L down to R
		# left half
		i = colTracker[column]
		#print i
		j = column
		#print j
		while((i > 0) and (j > 0)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i -= 1
			j -= 1
		# right half
		i = colTracker[column]
		j = column
		while((i < 5) and (j < 6)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i += 1
			j += 1
		count = 0
		# diagonal R down to L
		# left half
		i = colTracker[column]
		j = column
		while((i < 5) and (j > 0)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i += 1
			j -= 1
		# right half
		i = colTracker[column]
		j = column
		while((i > 0) and (j < 6)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i -= 1
			j += 1
		colTracker[column]-=1

		for i in range(0,6): # check column win
			if((count > 0) and (board[i][column] != p)): # reset counter if not consecutive
				count = 0
			if(board[i][column] == p):
				count += 1

			if count == 4: # WIN CONDITION MET
				winner = p
				return winner
		count = 0 # reset

		#print 'Current Winner ',winner
		return winner

def runPlayer(playerNum,playerVal):
    currentPlayer=players[playerNum];
    out1=(nonlin(np.dot(flatten(6,7,board,playerVal), currentPlayer[0])))
    out2=(nonlin(np.dot(out1,currentPlayer[1])))
    out=(nonlin(np.dot(out2,currentPlayer[2])))
    #print out
    m=out[0]
    index=0
    for x in range(1,7):
        if(out[x]>m):
            m=out[x]
            index=x
    return index

def play(playerA,playerB):
    reset()
    player=1
    w=0
    out=-1
    while(w==0):
        #for p in range(6):
        #	print board[p][0],"\t",board[p][1],"\t",board[p][2],"\t",board[p][3],"\t",board[p][4],"\t",board[p][5],"\t",board[p][6]
        #print "\n"
        if(player==1):
            w=addPiece(runPlayer(playerA,1), player)
        else:
            w=addPiece(runPlayer(playerA,-1), player)
    	player *= -1


    if(w==1):
        out=playerA
    else:
        out=playerB

    #print out,"won"

    return out

def train():
    for x in range(1000000):
        k=tournament()
        gen(k[0],k[1])
        if (x%100==0):
            print(x)
        if(x%1000==999):
            out=flattenPlayer(0)
            csvOut=[]
            for i in range(len(out)):
                csvOut.append(str(out[i]))
            with open("out2.csv","w+") as f:
                spamwriter = csv.writer(f, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

                spamwriter.writerow(csvOut)
            for row in players[0]:
                print "\t".join(csvOut)


def gen(playerA,playerB):
    	d = []
    	d.append(flattenPlayer(playerA))
    	d.append(flattenPlayer(playerB))
        d.append(d[0][:])
        d.append(d[1][:])
    	a = np.random.random(len(d[0]))
    	for l in range(len(d[0])):
    		if(a[l] > 0.5):
    			temp = d[2][l]
    			d[2][l] = d[3][l]
    			d[3][l] = temp*(np.random.random(1)[0]/5 +0.9)
                #temp is multiplied by a number between 0.9 and 1.1 for randomness
        for l in range(len(d)):
            d.append(d[l][:])
        for j in range(2):
    		a = np.random.random(len(d[0]))
    		for l in range(len(d[0])):
    			if(a[l] > 0.5):
    				temp = d[len(d)/2+j][l]
    				d[len(d)/2+j][l]=d[len(d)-j-1][l]
    				d[len(d)-j-1][l]=temp*(np.random.random(1)[0]/5 +0.9)
                    #temp is multiplied by a number between 0.9 and 1.1 for randomness
        for l in range(len(players)):
            players[l]=deflattenPlayer(d[l])

def flattenPlayer(playerNum):
    input=[]
    curr=flatten(42,20,players[playerNum][0])
    for k in curr:
        input.append(k)
    curr=flatten(20,20,players[playerNum][1])
    for k in curr:
        input.append(k)
    curr=flatten(20,7,players[playerNum][1])
    for k in curr:
        input.append(k)
    return input

def deflattenPlayer(arr):
    out=[]

    temp=[]
    for i in range(840):
        temp.append(arr[i])
    curr=deflatten(42,20,temp)
    out.append(curr)

    temp=[]
    for i in range(840,1240):
        temp.append(arr[i])
    curr=deflatten(20,20,temp)
    out.append(curr)

    temp=[]
    for i in range(1240,1380):
        temp.append(arr[i])
    curr=deflatten(20,7,temp)
    out.append(curr)

    return out;

def deflatten(x,y,arr):
    out=[]
    for a in range(x):
        o=[]
        for b in range(y):
            o.append(arr[(a*y)+b])
        out.append(o)
    return out

def flatten(x,y,arr,pval=1):
    out=[]
    for a in range(x):
        for b in range(y):
            out.append(pval*arr[a][b])
    return out

def tournament():
    contestants=[]
    for k in range(len(players)):
        contestants.append(k)
    winners = []
    while (len(contestants)>2):
        winners = []
        for k in range(len(contestants)/2):
            winners.append(play(contestants[k], contestants[len(contestants)-k-1]))
        contestants=winners
    #print winners
    return winners

def reset():
    for i in range(7):
        colTracker[i]=5
    for row in range(6):
        for col in range(7):
            board[row][col]=0

def demo(playerA,playerB):
    reset()
    player=1
    w=0
    out=-1
    while(w==0):
        for p in range(1,8):
            out=[]

        for p in range(6):
        	print board[p][0],"\t",board[p][1],"\t",board[p][2],"\t",board[p][3],"\t",board[p][4],"\t",board[p][5],"\t",board[p][6]
        time.sleep(1)
        print "\n"
        if(player==1):
            w=addPiece(runPlayer(playerA,1), player)
        else:

            print "Choose your column (1-7)"
            r=raw_input()
            w=addPiece(int(r)-1, player)

            #w=addPiece(runPlayer(playerB,-1), player)
    	player *= -1


    for p in range(6):
        print board[p][0],"\t",board[p][1],"\t",board[p][2],"\t",board[p][3],"\t",board[p][4],"\t",board[p][5],"\t",board[p][6]

    if(w==1):
        print "playerA won"
    else:
        print "playerB won"

def run():
    train()
    #demo(7,7)
    print('done')

def init():
    numIn=42
    numOut=7
    numPlayers=8
    for i in range(0,6): # rows
    	board.append([])
    	for j in range(0,7): # columns
    		board[i].append(0)
    for i in range(7):
        colTracker.append(5)
    for k in range(numPlayers-1):# Use numPlayers-1 when loading from csv
        p=[]
        p.append(2*np.random.random((numIn,20))-1)
        p.append(2*np.random.random((20,20))-1)
        p.append(2*np.random.random((20,numOut))-1)

        players.append(p);
    r=[]
    with open("out2.csv","r") as f:
        spamreader = csv.reader(f, delimiter=',', quotechar='|')
        for row in spamreader:
            for item in row:
                r.append(float(item))
    players.append(deflattenPlayer(r))


if __name__ == '__main__':
    init()
    run()
