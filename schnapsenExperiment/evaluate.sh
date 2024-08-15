#!/bin/bash

# Paths to the agent models
agent1_path=""
agent2_path=""
agent3_path=""

# Set the log directory for the current iteration
moreDataPath=""

# Function to run the evaluation and log the results
run_evaluation() {
  local agent=$1
  local opponent=$2

  echo "===================" >> $moreDataPath
  echo "Agent path $agent against $opponent" >> $moreDataPath
  echo "===================" >> $moreDataPath

  python schnapsenEvaluate.py \
    --seed=42 \
    --num_games=1000 \
    --moreDataPath=$moreDataPath \
    --opponent_path=$opponent \
    --agent_path=$agent
}

# Run each agent against an empty opponent path
run_evaluation $agent1_path ""
run_evaluation $agent2_path ""
run_evaluation $agent3_path ""

# Run each pair of agents against each other
run_evaluation $agent1_path $agent2_path
run_evaluation $agent1_path $agent3_path
run_evaluation $agent2_path $agent3_path
