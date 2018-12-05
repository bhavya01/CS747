# 1st argument: 0 for 4 actions, 1 for 8 actions
# 2nd argument: 0 for deterministic winds, 1 for stochastic
# 3rd argument: number of episodes
# 4th argument: output data file

python3 gridworld.py 0 0 200 dat1.pkl
python3 gridworld.py 1 0 500 dat2.pkl
python3 gridworld.py 1 1 1000 dat3.pkl
