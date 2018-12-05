import numpy as np
import sys

NROWS = 7
NCOLS = 10
WIND = [0,0,0,1,1,1,2,2,1,0]
GOAL = (3,7)
NUM_ACTIONS = 4
INIT_STATE = (3,0)
discount=1

# Parameters
alpha = 0.5
mode = int(sys.argv[1])
if mode == 1:
	NUM_ACTIONS = 8
stochastic = int(sys.argv[2])

NUM_EPS = int(sys.argv[3])
file = sys.argv[4]

def get_action(state,Q_value,epsilon,mode=0):
	# Action codes:
	# 0 for UP, 1 for RIGHT, 2 for DOWN, 3 for LEFT, 4 for UP RIGHT, 5 for RIGHT DOWN, 6 for DOWN LEFT, 7 for UP LEFT
	if mode == 0:
		valid_actions = [0,1,2,3]
	elif mode == 1:
		valid_actions = [0,1,2,3,4,5,6,7]
	r = state[0]
	c = state[1]
	# if r < NROWS-1:
	# 	valid_actions.append(0)
	# if c < NCOLS-1:
	# 	valid_actions.append(1)
	# if r > 0:
	# 	valid_actions.append(2)
	# if c > 0:
	# 	valid_actions.append(3)

	t=np.random.uniform()
	if t < epsilon:
		#explore
		return np.random.choice(valid_actions)
	else:
		#exploit
		max_action = -1
		max_val = -10000
		for a in valid_actions:
			if(Q_value[r][c][a] > max_val):
				max_val = Q_value[r][c][a]
				max_action = a
		return max_action

def get_next_state(s,a,stochastic=0):
	r = s[0]
	c = s[1]
	w_speed = WIND[c]
	if a == 0:
		r += 1
	elif a == 1:
		c += 1
	elif a == 2:
		r -= 1
	elif a == 3:
		c -= 1
	elif a == 4:
		r += 1; c+=1;
	elif a == 5:
		r-=1;c+=1
	elif a == 6:
		r-=1;c-=1;
	elif a == 7:
		r+=1;c-=1;

	r += w_speed

	if stochastic == 1:
		r += np.random.choice([-1,0,1])

	if r >= NROWS:
		r = NROWS-1
	if r < 0:
		r = 0
	if c >= NCOLS:
		c = NCOLS-1
	if c < 0:
		c = 0
	return (r,c)

def get_episode_outcome(Q_value,epsilon,mode,stochastic):
	t = 0
	s = INIT_STATE
	a = get_action(s,Q_value,epsilon,mode)
	while(s != GOAL):
		reward = -1
		ns = get_next_state(s,a,stochastic)
		na = get_action(ns,Q_value,epsilon,mode)
		Q_value[s[0]][s[1]][a] = alpha*(reward + discount*Q_value[ns[0]][ns[1]][na]) + (1-alpha)*Q_value[s[0]][s[1]][a]
		t +=1
		s = ns
		a = na
	return t

runs = []
random_seeds = range(10)

def optimal_policy(Q_value,mode):
	for r in range(NROWS):
		s = ""
		for c in range(NCOLS):
			s+= str(int(Q_value[r][c][get_action((r,c),Q_value,0,mode)])) + " "
		print(s)

for r_seed in random_seeds:

	np.random.seed(r_seed)

	Q_value = np.zeros((NROWS,NCOLS,NUM_ACTIONS))
	total_time = [0]

	for eps in range(NUM_EPS):
		epsilon = 0.5/(eps+1)
		t = get_episode_outcome(Q_value,epsilon,mode,stochastic)
		total_time.append(total_time[-1] + t)

	runs.append(total_time)

	print("random seed " + str(r_seed))
	print("Final greedy policy: ",get_episode_outcome(Q_value,0,mode,stochastic))
	optimal_policy(Q_value,mode)
runs = np.array(runs)
avg = np.mean(runs,axis=0)

import pickle;
with open(file,'wb') as f:
	pickle.dump(avg,f)

import matplotlib.pyplot as plt
plt.plot(avg,range(avg.shape[0]));plt.xlabel('Time steps'); plt.ylabel('Episodes')
plt.show()
