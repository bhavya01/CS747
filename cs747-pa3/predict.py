import sys
import numpy as np
import matplotlib.pyplot as plt
filename = sys.argv[1]

with open(filename,'r') as f:
    lines = f.readlines()

f2 = sys.argv[2]

with open(f2,'r') as f:
    l2 = f.readlines()

lambd = 0.9;
index=0
num_states = int(lines[index].split()[0]); index += 1;
value_func = [np.random.rand() for i in range(num_states)]
e = [0]*num_states
num_actions = int(lines[index].split()[0]); index += 1;

discount = float(lines[index].split()[0]); index += 1
a = [lines[i].split() for i in range(index,len(lines))]



for i in range(index,len(a)-1):
    s = int(a[i][0])
    ac = int(a[i][1])
    r = float(a[i][2])
    ns = int(a[i+1][0])
    d =  r + discount*value_func[ns] - value_func[s]
    e[s] += 1
    for j in range(num_states):
        value_func[j] = value_func[j] + 1/i*d*e[j]
        e[j] = e[j]*discount*lambd

for i in range(num_states):
    print(value_func[i])

error = 0
for i in range(num_states):
    error += (float(l2[i].split()[0]) -  value_func[i])**2
print(error)
