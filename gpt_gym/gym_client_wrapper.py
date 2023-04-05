impprt gymnasium as gym

class GymClientWrapper(gym.Client):
    def __init__(self, *args, **kwargs):
        super(GymClientWrapper, self).__init__(*args, **kwargs)
        self._env = None

    def make(self, env_id):
        self._env = super(GymClientWrapper, self).make(env_id)
        return self._env

    def reset(self):
        return self._env.reset()

    def step(self, action):
        return self._env.step(action)

    def render(self, mode='human'):
        return self._env.render(mode=mode)

    def close(self):
        return self._env.close()

    def seed(self, seed=None):
        return self._env.seed(seed)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()