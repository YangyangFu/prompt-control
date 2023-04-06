import gymnasium as gym
import requests
import json


class GymClient():
    def __init__(self, server_url):
        self.server_url = server_url

    def make_env(self, env_id):
        env_data = {
            'env_id': env_id
        }
        response = requests.post(self.server_url + '/v1/envs/', json=env_data)
        response_json = response.json()

        instance_id = response_json['instance_id']
        remote_env = RemoteEnvironment(self.server_url, instance_id)
        return remote_env


class RemoteEnvironment():
    def __init__(self, server_url, instance_id):
        self.server_url = server_url
        self.instance_id = instance_id

    def reset(self):
        response = requests.post(
            self.server_url + '/v1/envs/' + self.instance_id + '/reset/')
        response_json = response.json()
        return response_json['observation']

    def step(self, action):
        step_data = {
            'action': action
        }
        response = requests.post(
            self.server_url + '/v1/envs/' + self.instance_id + '/step/', json=step_data)
        response_json = response.json()
        return response_json['observation'], response_json['reward'], response_json['done'], response_json['info']

# Example Usage\n
if __name__ == '__main__':
    client = GymClient('http://127.0.0.1:5000')
    remote_env = client.make_env('CartPole-v0')

    obs = remote_env.reset()
    print(obs)

    for i in range(100):
        action = remote_env.action_space.sample()
        obs, reward, done, info = remote_env.step(action)
        print(obs, reward, done, info)
        if done:
            break
