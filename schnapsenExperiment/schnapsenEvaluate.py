''' An example of evluating the trained models in RLCard
'''
import os
import argparse
import torch

import rlcard
from rlcard.agents import (
    DQNAgent,
    RandomAgent,
)
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)


def evaluate(args):

    # Check whether gpu is available
    device = get_device()
        
    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlcard.make('schnapsen', config={'seed': args.seed})

    # Load models
    if args.agent_path != "":
        agent = torch.load(args.agent_path, map_location=device)
        agent.set_device(device)
    else:
        agent =  RandomAgent(num_actions=env.num_actions)
    if args.opponent_path != "":
        agent2 = torch.load(args.opponent_path, map_location=device)
        agent2.set_device(device)
    else:
        agent2 = RandomAgent(num_actions=env.num_actions)

    agents = [agent]

    agents.append(agent2)

    env.set_agents(agents)

    # Evaluate
    rewards = tournament(env, args.num_games, args.moreDataPath)

    print("player",  rewards[0])
    print("Opponent",  rewards[1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Evaluation example in RLCard")

    parser.add_argument(
        '--agent_path',
        type=str,
        default= '',
    )
    parser.add_argument(
        '--opponent_path',
        type=str,
        default= '',
    )
    parser.add_argument(
        "--moreDataPath",
        type=str,
        default="",
    )

    parser.add_argument(
        '--cuda',
        type=str,
        default='',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=484,
    )
    parser.add_argument(
        '--num_games',
        type=int,
        default=100,
    )

    args = parser.parse_args()

    #os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    evaluate(args)

