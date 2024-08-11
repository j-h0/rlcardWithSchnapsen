#!/bin/bash

# Initial values
learning_rate=0.01
discount_factor=0.8
replay_memory_size=30000

# Paths
training_agent_path="/home/erpl/Documents/MCI/bachelor/restart/rlcard/rlcardWithSchnapsen/rlcardWithSchnapsen/schnapsenExperiment/logdir_training_1/checkpoint_dqn.pt"
opponent_agent_path="/home/erpl/Documents/MCI/bachelor/restart/rlcard/rlcardWithSchnapsen/rlcardWithSchnapsen/schnapsenExperiment/logdir+0.001+0.8+/checkpoint_dqn.pt"
log_dir_base="logdir_training"


  # Set the log directory for the current iteration
log_dir="${log_dir_base}_2"

# Run the Python script
python schnapsentest.py \
  --learning_rate=$learning_rate \
  --discount_factor=$discount_factor \
  --replay_memory_size=$replay_memory_size \
  --log_dir=$log_dir \
  --num_episodes=5000 \
  --num_eval_games=500 \
  --seed=43 \
  --evaluate_every=100 \
  --moreDataPath=/home/erpl/Documents/MCI/bachelor/restart/rlcard/rlcardWithSchnapsen/rlcardWithSchnapsen/schnapsenExperiment/training.txt \
  --training_agent=$training_agent_path \
  --opponent_agent=$opponent_agent_path



