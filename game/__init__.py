from gym.envs.registration import register

register(
    id='Pygame-v0',
    entry_point='game.envs.custom_env:CustomEnv',
    max_episode_steps=100000
)