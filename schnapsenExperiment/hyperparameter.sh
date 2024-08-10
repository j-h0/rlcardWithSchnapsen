#!/bin/bash

# Check if the file path argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <result_file_path>"
    exit 1
fi

# Use the provided argument as the path to the tournament_results.txt file
result_file="$1"

# Debugging output: Print the result file path
echo "Writing results to: $result_file"

for i in 0.01 0.001 0.0001 0.00001; do
    for j in 0.7 0.8 0.9 ; do
        # Debugging output: Print the current combination
        echo "Processing combination: learning_rate=$i, discount_factor=$j"

        # Log a new line and a separator before logging the combination
        echo -e "\n==========================" >> "$result_file"
        echo "Combination: learning_rate=$i, discount_factor=$j" >> "$result_file"
        
        # Run the Python script with the current combination of parameters
        python schnapsentest.py --learning_rate=$i --discount_factor=$j --replay_memory_size=20000 --log_dir=logdir+$i+$j+ --num_episodes=2000 --num_eval_games=500 --seed=42 --evaluate_every=100
    done
done
