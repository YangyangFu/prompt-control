import gymnasium as gym
import socket
import json
import time

# Constants
HOST = '127.0.0.1'
PORT = 65432

# Functions
def process_ai_response(response):
    if 'left' in response.lower():
        return 0
    else:
        return 1

# Main
env = gym.make('CartPole-v1', render_mode='human')
state, _ = env.reset()
done = False
total_reward = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Gym environment client is listening...")

    conn, addr = s.accept()
    with conn:
        print('Connected to GPT process:', addr)
        while not done:
            data = conn.recv(1024)
            if not data:
                break

            command = json.loads(data.decode('utf-8'))
            action = process_ai_response(command['text'])
            state, reward, done, _, _ = env.step(action)
            total_reward += reward
            env.render()
            time.sleep(0.1)

        conn.sendall(b'done')

env.close()
print("Total reward:", total_reward)
