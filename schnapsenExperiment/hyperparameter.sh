#!/bin/bash


for i in 0.01 0.001 0.0001; do
    for j in 0.8 0.9 1; do
        for k in 20000 30000 50000; do
            python schnapsentest.py --learning_rate=$i --discount_factor=$j --replay_memory_size=$k --log_dir=logdir+$i+$j+$k
        done
    done
done

