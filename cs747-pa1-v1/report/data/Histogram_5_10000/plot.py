import matplotlib.pyplot as plt
import csv
import numpy as np

# e0 is with 0.05
# e1 is with 0.1
# e2 is with 0.2
# e3 is with 0.4
# e4 is with 0.6
#UCB best arm = 4;
#KL-UCB best arm =
# Thompson best arm=
dirs = ['e0','e1','e2','e3','e4','UCB','Thompson']
x = []
for d in dirs:
	y = []
	for j in range(1,101):
		with open(d + '/clientlog' + str(j) +'.txt','r') as csvfile:
			plots = csv.reader(csvfile, delimiter=',')
			for r in plots:
				y.append([i*0.777777778 - float(r[i]) for i in range(len(r))])
	y = np.array(y)
	print(y.shape)
	y = np.sum(y,axis=0)/100
	x.append(y)

for i in range(len(x)):
	plt.plot(x[i],label=dirs[i])
plt.legend()
plt.show()
