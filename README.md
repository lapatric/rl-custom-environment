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

## Registering Envs

In order for the custom environments to be detected by Gymnasium, they must be registered as follows. We will choose to put this code in `src/__init__.py`.

```python
from gymnasium.envs.registration import register

register(
     id="gym_examples/GridWorld-v0",
     entry_point="gym_examples.envs:GridWorldEnv",
     max_episode_steps=300,
)
```

The environment ID consists of three components, two of which are optional: an optional namespace (here: `src`), a mandatory name (here: `GridWorld`) and an optional but recommended version (here: `v0`). It might have also been registered as `GridWorld-v0` (the recommended approach), `GridWorld` or `src/GridWorld`, and the appropriate ID should then be used during environment creation.

The keyword argument `max_episode_steps=300` will ensure that GridWorld environments that are instantiated via `gymnasium.make` will be wrapped in a `TimeLimit` wrapper (see the wrapper documentation for more information). A done signal will then be produced if the agent has reached the target or 300 steps have been executed in the current episode. To distinguish truncation and termination, you can check `info["TimeLimit.truncated"]`.

Apart from id and entrypoint, you may pass the following additional keyword arguments to register:

| Name | Type | Default | Description |
|---|---|---|---|
| `reward_threshold` | `float` | `None` | The reward threshold before the task is considered solved |
| `nondeterministic` | `bool` | `False` | Whether this environment is non-deterministic even after seeding |
| `max_episode_steps` | `int` | `None` | The maximum number of steps that an episode can consist of. If not `None`, a `Timelimit` wrapper is added |
| `reward_threshold` | `float` | `None` | Whether to wrap the environment in an `OrderEnforcing` wrapper |
| `reward_threshold` | `float` | `None` | Whether to wrap the environment in an `AutoResetWrapper` |
| `reward_threshold` | `float` | `None` | The default kwargs to pass to the environment class |

Most of these keywords (except for max_episode_steps, order_enforce and kwargs) do not alter the behavior of environment instances but merely provide some extra information about your environment.

After registration, our custom GridWorldEnv environment can be created with `env = gymnasium.make('gym_examples/GridWorld-v0')`.
`src/envs/__init__.py` should have:
```python
from src.envs.grid_world import GridWorldEnv
```
For more details refer to the [tutorial documentation](https://gymnasium.farama.org/tutorials/environment_creation/).