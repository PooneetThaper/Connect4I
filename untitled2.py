# INITIALIZATION

winner = 0
board = []
for i in range(0,6): # rows
	board.append([])
	for j in range(0,7): # columns
		board[i].append(0)
for p in range(6):
	print board[p]

player = 1


def addPiece(column, player):
	count = 0
	for i in range(5,-1,-1): # iterate rows to add piece

		if(board[i][column] == 0): # checking for empty row to place
			board[i][column] = player 
			
			for j in range(0, 7): # check row win
				if((count > 0) and (board[i][j] != player)): # reset counter if not consecutive
					count = 0
				if(board[i][j] == player):
					count += 1

				if(count == 4): # WIN CONDITION MET
					winner = player
					print winner,' won'
					''' Cleaning up
					for l in range(0,7): # column
						for k in range(0,6): # row
							if((board[k][l] != player) and (board[k][l] != 0)): # replace with winner
								board[k][l] = 0
					'''
					return
			break
		elif(i == 0): # LOSE CONDITION MET
			winner = -1*player
			'''
			for k in range(0,7): #column
				for j in range(0,6): #row
					board[j][k] = -1
			'''
			return
	count = 0 # reset
	# check win conditions
	for i in range(0,6): # check column win
		if((count > 0) and (board[i][column] != player)): # reset counter if not consecutive
			count = 0
		if(board[i][column] == player):
			count += 1

		if count == 4: # WIN CONDITION MET
			winner = player
			print winner,' won'
			''' Cleaning up
			for k in range(0,7): # column
				for j in range(0,6): # row
					if((board[j][k] != player) and (board[j][k] != 0)): # replace with winner 
						board[j][k] = 0
			'''
			return
	count = 0 # reset
	

	return


while(True):
	print 'gimme dat column boi'
	column = int(raw_input())
	print 'its ',player,'\'s  turn'
	addPiece(column, player)
	player *= -1
	for p in range(6):
		print board[p]