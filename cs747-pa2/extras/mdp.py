
"""
MDP Planning using LP and Howard's Policy Iterations

Author: Bhavya Bahl 2018
"""
# For the episodic MDPSs it is assumed that the last state in the terminal state
import sys
from pulp import *

if(len(sys.argv) != 3):
	print("Usage: python mdp.py filename algorithm")
	sys.exit()


filename = sys.argv[1]
algorithm = sys.argv[2]

with open(filename) as f:
	lines = f.readlines()

index=0
states = lines[index].split()
states = int(states[0])
index+=1

actions = lines[index].split()
actions = int(actions[0])
index +=1


rewards = []
for s in range(states):
	rewards.append(list([]))
	for a in range(actions):
		rewards[s].append(list([]))
		r = lines[index].split()
		for i in r:
			rewards[s][a].append(float(i))
		index += 1

transitions = []
for s in range(states):
	transitions.append(list([]))
	for a in range(actions):
		transitions[s].append(list([]))
		r = lines[index].split()
		for i in r:
			transitions[s][a].append(float(i))
		index += 1

discount = lines[index].split()
discount = float(discount[0])
index += 1

cont = lines[index].split()
if(cont[0] == 'continuing'):
	cont = 1
else:
	cont = 0

if algorithm == 'lp':
	prob = LpProblem("MDP", LpMinimize)
	state_vals = LpVariable.dicts("Value",range(states))

	prob += lpSum([state_vals[i] for i in range(states)])
	for s in range(states):
		if cont == 0:
			if s == states -1:
				prob += state_vals[s] == 0.0
		for a in range(actions):
			prob += state_vals[s] >= lpSum( [transitions[s][a][s1]*(rewards[s][a][s1] + discount*state_vals[s1] ) for s1 in range(states)])

	prob.solve()

	#Finding actions for the value function
	state_actions = []
	for s in range(states):
		for a in range(actions):
			v = 0
			for s1 in range(states):
				v += transitions[s][a][s1]*(rewards[s][a][s1] + discount*state_vals[s1].value())
			if(abs(v - state_vals[s].value()) < 1e-6):
				print(str(state_vals[s].value()) + "\t"+str(a))
				break

elif algorithm == 'hpi':
	policy = [0]*states
	change = 1
	while(change):
		change = 0
		#Find the value function given the actions
		prob= LpProblem("MDP")
		state_vals = LpVariable.dicts("Value", range(states))

		for s in range(states):
			if cont == 0 and s == states -1:
				prob += state_vals[states-1] == 0.0
			else:
				prob += state_vals[s] == lpSum([transitions[s][policy[s]][s1]*(rewards[s][policy[s]][s1] + discount*state_vals[s1]) for s1 in range(states)])

		prob.solve()
		#If an improving action is found change the policy
		for s in range(states):
			if cont == 0 and s == states-1 :
				continue
			for a in range(actions):
				v = 0
				for s1 in range(states):
					v += transitions[s][a][s1]*(rewards[s][a][s1] + discount*state_vals[s1].value())
				if(v > state_vals[s].value() + 1e-6):
					policy[s] = a
					change = 1
					break

	#Given the optimal policy, find the optimal value function
	prob= LpProblem("MDP")
	state_vals = LpVariable.dicts("Value", range(states))
	for s in range(states):
		if cont == 0 and s == states -1:
			prob += state_vals[states-1] == 0.0
		else:
			prob += state_vals[s] == lpSum([transitions[s][policy[s]][s1]*(rewards[s][policy[s]][s1] + discount*state_vals[s1]) for s1 in range(states)])

	prob.solve()

	for s in range(states):
		print(str(state_vals[s].value()) + "\t" + str(policy[s]))

	with open("./results.csv", "a") as myfile:
		for s in range(states):
			if s == states -1:
				myfile.write(str(state_vals[s].value()))
			else :
				myfile.write(str(state_vals[s].value()) + ",")
		myfile.write("\n")

	with open("./actions.csv", "a") as myfile:
		for s in range(states):
			if s == states -1:
				myfile.write(str(policy[s]))
			else :
				myfile.write(str(policy[s]) + ",")
		myfile.write("\n")
