import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the base directory and the subdirectories for each hyperparameter setting
base_dir = "/home/erpl/Documents/MCI/bachelor/restart/rlcard/rlcardWithSchnapsen/rlcardWithSchnapsen/schnapsenExperiment/"
sub_dirs = [
    "logdir+0.00001+0.7+",
    "logdir+0.0001+0.7+",
    "logdir+0.001+0.7+",
    "logdir+0.01+0.7+",
    "logdir+0.00001+0.8+",
    "logdir+0.0001+0.8+",
    "logdir+0.001+0.8+",
    "logdir+0.01+0.8+",
    "logdir+0.00001+0.9+",
    "logdir+0.0001+0.9+",
    "logdir+0.001+0.9+",
    "logdir+0.01+0.9+"
]

# Initialize a dictionary to store data from each configuration
data_dict = {}

# Loop through each directory, load the CSV, and store the data
for sub_dir in sub_dirs:
    csv_path = os.path.join(base_dir, sub_dir, "performance.csv")
    
    if os.path.exists(csv_path):
        # Load the CSV file
        df = pd.read_csv(csv_path)
        
        # Assume that 'episode' is in the first column and 'reward' is in the second column
        episodes = df.iloc[:, 0]
        rewards = df.iloc[:, 1]
        
        # Store the data in the dictionary
        data_dict[sub_dir] = (episodes, rewards)
    else:
        print(f"File not found: {csv_path}")

# Plotting the data
plt.figure(figsize=(12, 8))

for config, (episodes, rewards) in data_dict.items():
    if config == "logdir+0.01+0.8+":
        plt.plot(episodes, rewards, label=config, color='red', linewidth=3)  # Emphasize this line
    if config == "logdir+0.01+0.7+":
        plt.plot(episodes, rewards, label=config, color='blue', linewidth=3)  # Emphasize this line
    else:
        plt.plot(episodes, rewards, label=config, linewidth=1, alpha=0.6)  # De-emphasize others


plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Comparison of DQN Performance Across Hyperparameter Configurations')
plt.legend(loc='best', fontsize='small')
plt.grid(True)
plt.show()
