# RLCardWithSchnapsen

This repository is a fork of [RLCard](https://github.com/datamllab/rlcard), extended to include the Schnapsen card game. RLCard is a toolkit for developing reinforcement learning environments for card games.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/j-h0/rlcardWithSchnapsen
cd rlcardWithSchnapsen
```

### Setting Up a Virtual Environment

To ensure a clean and isolated environment for managing dependencies, it's recommended to use a Python virtual environment (`venv`). This will help you avoid conflicts between the packages required for this project and those in your global Python environment.

Before installing dependencies, create and activate a virtual environment:

```bash
# Create a virtual environment in the directory 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate 
```

After activating the virtual environment, proceed with the installation of the necessary dependencies:

```bash
pip3 install -e .
pip3 install -e .[torch]
```

## Usage

After installation, you can start using the environment to train and evaluate reinforcement learning algorithms.

Start by familiarizing yourself with the repository, including the original codebase.

Use hyperparameter.sh for hyperparameter grid search

training.sh with different values to train a Schnapsen agent

## License

Licensed under the [MIT License](https://github.com/j-h0/rlcardWithSchnapsen/blob/master/LICENSE.md).

---

This repository is maintained as part of a bachelor's thesis project focused on applying reinforcement learning to Schnapsen.
