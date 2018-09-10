import csv
import matplotlib.pyplot as plt

values = []
actions = []
with open("results.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        y = [float(i) for i in row]
        values.append(y)

with open("actions.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        y = [float(i) for i in row]
        actions.append(y)

ph = [0.2,0.4,0.6,0.8]
for v in range(len(values)):
    plt.plot(values[v],label="ph="+str(ph[v]))

plt.ylabel('Value estimates')
plt.xlabel('states')

plt.legend(loc=4)
plt.show()

for v in range(len(values)):
    plt.plot(actions[v],label="ph="+str(ph[v]))

plt.ylabel('Optimal actions')
plt.xlabel('states')

plt.legend(loc=1)
plt.show()
