''' training a reinforcement learning agent on the environment schnapsen in RLCard
'''
import os
import argparse

import torch
import time

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    reorganize,
    Logger,
    plot_curve,
)

def train(args):

    # Check whether gpu is available
    device = get_device()
        
    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlcard.make(
        "schnapsen",
        config={
            'seed': args.seed,
        }
    )

    # Initialize the agent and use random agents as opponents
    from rlcard.agents import DQNAgent
    if args.load_checkpoint_path != "":
        agent2 =DQNAgent.from_checkpoint(checkpoint=torch.load('schnapsenExperiment/logdir+0.01+0.8+20000/checkpoint_dqn.pt',map_location=device))
        agent = DQNAgent.from_checkpoint(checkpoint=torch.load('schnapsenExperiment/logdir+0.0001+1+30000/checkpoint_dqn.pt',map_location=device))
    else:
        agent = DQNAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            mlp_layers=[64,64],
            device=device,
            save_path=args.log_dir,
            save_every=args.save_every,
            replay_memory_size = args.replay_memory_size,
            learning_rate= args.learning_rate,
            discount_factor= args.discount_factor,
        )
        agent2 = RandomAgent(num_actions=env.num_actions)

    agents = [agent]

    agents.append(agent2)

    env.set_agents(agents)

    # Start training
    with Logger(args.log_dir) as logger:
        for episode in range(args.num_episodes):

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            # Here, we assume that DQN always plays the first position
            # and the other players play randomly (if any)
            for ts in trajectories[0]:
                agent.feed(ts)

            # Evaluate the performance. Play with random agents.
            if episode % args.evaluate_every == 0:
                logger.log_performance(
                    episode,
                    tournament(
                        env,
                        args.num_eval_games,
                    )[0]
                )


        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, "DQN")

    # Save model
    save_path = os.path.join(args.log_dir, 'model.pth')
    torch.save(agent, save_path)
    print('Model saved in', save_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("DQN with Schnapsen")

    parser.add_argument(
        '--cuda',
        type=str,
        default='',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
    )
    parser.add_argument(
        '--num_episodes',
        type=int,
        default=1000,
    )
    parser.add_argument(
        '--num_eval_games',
        type=int,
        default=100,
    )
    parser.add_argument(
        '--evaluate_every',
        type=int,
        default=50,
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default='experiments/training_logdirNew/',
    )
    
    parser.add_argument(
        "--load_checkpoint_path",
        type=str,
        default="",
    )
    
    parser.add_argument(
        "--save_every",
        type=int,
        default=-1,
    )
    
    parser.add_argument(
        "--discount_factor",
        type = float,
        default= 0.99,
    )

    parser.add_argument(
        "--learning_rate",
        type = float,
        default= 0.00005,
    )
    
    parser.add_argument(
        "--replay_memory_size",
        type = int,
        default= 20000,
    )

    args = parser.parse_args()

# because of reasons unknown to me this call produces problems with the nvidia driver
#   os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda 
    start_time = time.time()
    train(args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

