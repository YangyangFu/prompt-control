import logging
import random

from gym_client import ClientWrapper
from agents import RandomDiscreteAgent

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Set up client
    remote_base = 'http://127.0.0.1:5000'
    client = ClientWrapper(remote_base)

    # Set up environment
    instance_id, env_id = client.get_ids()

    # Set up agent
    action_space_info = client.env_action_space_info(instance_id)
    agent = RandomDiscreteAgent(action_space_info['n'])

    # Run experiment, with monitor
    #outdir = '/tmp/random-agent-results'
    #client.env_monitor_start(
    #    instance_id, outdir, force=True, resume=False, video_callable=False)

    episode_count = 10
    max_steps = 200
    reward = 0
    done = False

    for i in range(episode_count):
        ob = client.env_reset(instance_id)

        for j in range(max_steps):
            action = agent.act(ob, 0, done)
            print(action)
            ob, reward, done, _, _ = client.step(action)
            if done:
                break

    # Dump result info to disk
    #client.env_monitor_close(instance_id)

