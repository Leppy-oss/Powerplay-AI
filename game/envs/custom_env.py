import gym
from gym import spaces
import numpy as np
from game.src.main.game import Game

class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = Game()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.array([0]), np.array([1000]), dtype=np.int32)

    def reset(self):
        del self.pygame
        self.pygame = Game()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        if(self.pygame.reached_goal()):
            print('REACHED THE GOAL!!!')
            
        done = self.pygame.driver_failed() or self.pygame.reached_goal()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.render()