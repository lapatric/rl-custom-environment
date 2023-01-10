from gymnasium.envs.registration import register

register(
    id="src/GridWorld-v0",
    entry_points="src.envs:GridWorldEnv",
    max_episode_steps=300,
)