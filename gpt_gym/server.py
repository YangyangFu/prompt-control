import gymnasium as gym
import socket
import time 
import json

"""
This is to run gym environments in a separate process, and serve as a server for GPT clients

"""
# Constants
HOST = '127.0.0.1'
PORT = 5002

class GymServer():
    def __init__(self, env_id, host, port):
        self.host = host
        self.port = port
        self.env_id = env_id
        self.make_env(env_id)
        self.env.reset()

    def make_env(self, env_id):
        self.env = gym.make(env_id, render_mode='human')
    
    def make_socket(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
    
    def listen(self):
        self.s.listen()
        print("Gym environment server is listening...")
        self.conn, self.addr = self.s.accept()
        with self.conn:
        
            print('Connected to GPT process:', self.addr)
            while True:    
                data = self.conn.recv(1024)
                if not data:
                    return
                command = json.loads(data.decode('utf-8'))
                print(command)
                action = int(command['text'])
                # execute action
                self.observation, self.reward, self.done, self.truncated, self.info = self.env.step(action)
                # render
                self.env.render()
                
                # send back status
                self.conn.sendall(json.dumps({"observation": self.observation.tolist(), "reward": self.reward, "done": self.done, "truncated": self.truncated, "info": self.info}).encode('utf-8'))
                
                if self.done:
                    print("Experiment is done. Total reward:", self.reward)
                    print("We are reinitializing the experiment......")
                    self.env.reset()
                    print("Experiment is reinitialized.")

    def run(self):
        self.env = self.make_env(self.env_id)
        state, _ = self.env.reset()
        done = False
        total_reward = 0
        while not done:
            data = self.conn.recv(1024)
            if not data:
                break
            command = json.loads(data.decode('utf-8'))
            action = self.process_ai_response(command['text'])
            state, reward, done, _, _ = self.env.step(action)
            total_reward += reward
            self.env.render()
            time.sleep(0.1)
        self.conn.sendall(b'done')
        self.env.close()
        print("Total reward:", total_reward)

if __name__ == "__main__":
    env_id = 'CartPole-v1'
    gs = GymServer(env_id, HOST, PORT)
    gs.make_socket(HOST, PORT)
    gs.listen()
    #gs.run()