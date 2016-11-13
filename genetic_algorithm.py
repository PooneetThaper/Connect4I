import numpy as np

def main():
	players = []

	p1 = [0.5, 0.25, 0.1]
	p2 = [0.3, 0.6, 0.9]

	players.append(p1[:])
	players.append(p2[:])


	a = np.random.random(len(p1))
	print(a)

	for k in range(len(p1)):
		if(a[k] > 0.5):
			temp = p1[k]
			p1[k] = p2[k] 
			p2[k] = temp

	players.append(p1[:])
	players.append(p2[:])

	print(players)

	x = len(players)
	while(x != 2):
		for n in range(x/2):
			if(p1[n] == 1): #win
				p1[len(p1)-n] == 0 #corresponding loss
			elif(p1[n] == 0): #loss
				p1[len(p1)-n] == 1 #corresponding win
		x = x/2



if __name__ == '__main__':
	main()