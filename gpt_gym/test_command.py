import openai
import socket
import os
import json

# Constants
HOST = '127.0.0.1'
PORT = 5002

# Main
env_state = [0, 0, 0, 0]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        response = input(" -> ")  # take input
        s.sendall(json.dumps({"text": response}).encode('utf-8'))
        data = s.recv(1024)
        if data == b'done':
            break

print("GPT process has finished.")
