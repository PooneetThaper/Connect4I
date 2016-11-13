import numpy as np

def main():
	np.random.seed(2)
	d = []
	d.append([0.5, 0.25, 0.1])
	d.append([0.3, 0.6, 0.9])
	d.append(d[0][:])
	d.append(d[1][:])
	a = np.random.random(len(d[0]))
	print a
	for l in range(len(d[0])):
		if(a[l] > 0.3):
			temp = d[2][l]
			d[2][l] = d[3][l]
			d[3][l] = temp
	for l in range(len(d)):
		d.append(d[l][:])
	for j in range(2):
		a = np.random.random(len(d[0]))
		print a
		for l in range(len(d[0])):
			if(a[l] > 0.3):
				temp = d[len(d)/2+j][l]
				d[len(d)/2+j][l]=d[len(d)-j-1][l]
				d[len(d)-j-1][l]=temp
			elif(a[l] > 0.5):
				print "hi"
	print d


	print np.random.random(1)[0]

if __name__ == '__main__':
	main()
