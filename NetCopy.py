import numpy as np

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
		#Win Check
def runPlayer(playerNum):
	out=(nonlin(np.dot(flatten(6,7,board), players[playerNum])))
	m=out[0]
	index=0
	for x in range(1,7):
		if(out[x]>m):
			m=out[x]
			index=x
	return index

def play(playerA,playerB):
	player=1
	w=0
	while(w==0):
		#for p in range(6):
			#print board[p]
		if(player==1):
			w=addPiece(runPlayer(playerA), player)
		else:
			w=addPiece(runPlayer(playerA), player)
		player *= -1
	if(w==1):
		return playerA
	else:
		return playerB

def run():
	for x in range(2000):
		k=tournament()
		gen(k[0],k[1])

def gen(playerA,playerB):
		p=players[:]
		d = []
		d.append(flatten(42,7,players[playerA]))
		d.append(flatten(42,7,players[playerB]))
		d.append(d[0][:])
		d.append(d[1][:])
		a = np.random.random(len(d[0]))
		for l in range(len(d[0])):
			if(a[l] > 0.5):
				temp = d[2][l]
				d[2][l] = d[3][l]
				d[3][l] = temp*np.random.random(1)[0]*2
		for l in range(len(d)):
			d.append(d[l][:])
		for j in range(2):
			a = np.random.random(len(d[0]))
			for l in range(len(d[0])):
				if(a[l] > 0.5):
					temp = d[len(d)/2+j][l]
					d[len(d)/2+j][l]=d[len(d)-j-1][l]
					d[len(d)-j-1][l]=temp
		for l in range(len(players)):
			players[l]=deflatten(42,7,d[l])
		if d==p:
			print "wat"
		print 'k'

def deflatten(x,y,arr):
	out=[]
	for a in range(x):
		o=[]
		for b in range(y):
			o.append(arr[(a*y)+b])
		out.append(o)
	return out

def flatten(x,y,arr):
	out=[]
	for a in range(x):
		for b in range(y):
			out.append(arr[a][b])
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
	print winners
	return winners

def init():
	numIn=42
	numOut=7
	numPlayers=8
	np.random.seed(0)
	for i in range(0,6): # rows
		board.append([])
		for j in range(0,7): # columns
			board[i].append(0)
	for i in range(7):
		colTracker.append(5)
	for k in range(numPlayers):
		players.append(2*np.random.random((numIn,numOut))-1)

if __name__ == '__main__':
	init()
	run()