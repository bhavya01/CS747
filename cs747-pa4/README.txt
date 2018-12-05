To run all the cases execute the following command
./script.sh
This will also generate plots for the individual cases

To run the code for individual cases run the following command:
python3 gridworld.py <mode> <stochastic> <num_episodes> <output_file>
mode : 0 for 4 actions, 1 for 8 actions
stochastic : 0 for deterministic world, 1 for stochastic gridworld
num_episodes : number of episodes for which sarsa agent should run
output_file : the file to which the averaged (over random seeds) cumulative time steps for the episodes would be saved

The variable WIND in gridworld.py can be used to change the windspeeds for the task. The number of rows and number of columns is also specified in the gridworld.py file
