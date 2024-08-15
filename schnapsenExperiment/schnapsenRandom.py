''' An example of playing randomly in RLCard
'''
import argparse
import pprint

import torch

import rlcard
from rlcard.agents import RandomAgent, DQNAgent
from rlcard.utils import set_seed, get_device

def run(args):
    # Make environment
    env = rlcard.make(
        'schnapsen',
        config={
            'seed': 1,
        }
    )
    device = get_device()
        
    # Seed numpy, torch, random
    set_seed(1)

    # Load models
    if args.agent_path != "":
        agent = torch.load(args.agent_path, map_location=device)
        agent.set_device(device)
    else:
        agent =  RandomAgent(num_actions=env.num_actions)

    agent2 = RandomAgent(num_actions=env.num_actions)

    agents = [agent,agent2]
    env.set_agents(agents)

    # Generate data from the environment
    trajectories, player_wins = env.run(is_training=False)
    # Print out the trajectories

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Random example in RLCard")

    parser.add_argument(
        '--agent_path',
        type=str,
        default= '/home/erpl/Documents/MCI/bachelor/restart/rlcard/rlcardWithSchnapsen/rlcardWithSchnapsen/schnapsenExperiment/logdir_training_2/model.pth',
    )

    args = parser.parse_args()

    run(args)

