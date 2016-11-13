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


if __name__ == '__main__':
	main()