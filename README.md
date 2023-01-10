# Making a custom RL environment

This repository follows along with the tutorial from the OpenAI Gymnasium tutorial [Make your own custom environment](https://gymnasium.farama.org/tutorials/environment_creation/).

Begin by setting up the python environment for this tutorial. 

```bash
python -m venv .env
source .env/bin/activate
pip install -e .
```

## Subclassing gymnasium.Env

This environment implements a very simplistic game consisting of a 2-dimensional square grid of fixed size (specified via the size parameter during construction). The agent can move vertically or horizontally between grid cells in each timestep. The goal of the agent is to navigate to a target on the grid that has been placed randomly at the beginning of the episode.

- States (observations) provide the location of the target and agent.
- There are 4 actions in our environment, corresponding to the movements “right”, “up”, “left”, and “down”.
- A done signal is issued as soon as the agent has navigated to the grid cell where the target is located.
- Rewards are binary and sparse, meaning that the immediate reward is always zero, unless the agent has reached the target, then it is 1.

## Declaration and Initialization

Our custom environment will inherit from the abstract class `gymnasium.Env`. You shouldn’t forget to add the metadata attribute to your class. There, you should specify the render-modes that are supported by your environment (e.g. `"human"`, `"rgb_array"`, `"ansi"`) and the framerate at which your environment should be rendered. Every environment should support `None` as render-mode; you don’t need to add it in the metadata. In `GridWorldEnv`, we will support the modes “rgb_array” and “human” and render at 4 FPS.

The `__init__` method of our environment will accept the integer `size`, that determines the size of the square grid. We will set up some variables for rendering and define `self.observation_space` and `self.action_space`. In our case, observations should provide information about the location of the agent and target on the 2-dimensional grid. We will choose to represent observations in the form of dictionaries with keys `"agent"` and `"target"`. An observation may look like `{"agent": array([1, 0]), "target": array([0, 3])}`. Since we have 4 actions in our environment (“right”, “up”, “left”, “down”), we will use `Discrete(4)` as an action space. 