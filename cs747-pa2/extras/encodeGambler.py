import sys
if len(sys.argv) != 2:
    print("Usage: python encodeGambler.py <ph>")

ph = float(sys.argv[1])

states = 101
# Number of states goes from 0 to 100. 0 is a terminal state with value 0
# To make the value of state 100 equal to 1, we make a transition to state 0 with reward 1 for all actions
actions = 50
print(states)
print(actions)
for s in range(states):
    for a in range(actions):
        line = ""
        for s1 in range(states):
            if(s1 == 0):
                if (s == 100):
                    # If we reach our goal of 100 then we get our reward of 1 definitely
                    line += str(1) + "\t"
                else:
                    line += str(0) + "\t"
            else:
                line += str(0) + "\t"
        print(line)

for s in range(states):
    for a in range(1,actions+1):
        # a ranges from 1 to 50
        line = ""
        for s1 in range(states):
            if s == 0:
                #For state 0, all actions endup in state 0 with reward 0
                if(s1 == 0):
                    line += str(1) + "\t"
                else:
                    line += str(0) + "\t"
            elif s == 100:
                #For state 100, all actions endup in state 0 with reward 1
                if(s1 == 0):
                    line += str(1) + "\t"
                else:
                    line += str(0) + "\t"
            elif(a > min(s,100-s)):
                if (s1 == 0):
                    # If the action is not allowed MDP goes to a state 0 with zero reward
                    line += str(1) + "\t"
                else:
                    line += str(0) + "\t"
            else:
                if (s1 == s + a):
                    line += str(ph) + "\t"
                elif (s1 == s-a):
                    line += str(1 - ph) + "\t"
                else:
                    line += str(0) + "\t"
        print(line)

print(0.999)
print("episodic")
