#!/bin/bash

# Initial values
learning_rate=0.0005
discount_factor=0.99
replay_memory_size=100000

# Paths
training_agent_path=""
opponent_agent_path=""
log_dir_base="logdir_training"
moreDataPath=""


  # Set the log directory for the current iteration
log_dir="${log_dir_base}_4"

# Run the Python script
python schnapsentest.py \
  --learning_rate=$learning_rate \
  --discount_factor=$discount_factor \
  --replay_memory_size=$replay_memory_size \
  --log_dir=$log_dir \
  --num_episodes=10000 \
  --num_eval_games=500 \
  --seed=45 \
  --evaluate_every=100 \
  --moreDataPath=$moreDataPath \
  --opponent_agent=$opponent_agent_path \

  


