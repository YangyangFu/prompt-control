import openai
import socket
import os
import json

# Constants
HOST = '127.0.0.1'
PORT = 65432

# Functions
def create_prompt(state):
    cart_position, cart_velocity, pole_angle, pole_velocity = state
    prompt = f"The cart's position is {cart_position:.2f}, its velocity is {cart_velocity:.2f}, the pole's angle is {pole_angle:.2f}, and its angular velocity is {pole_velocity:.2f}. Should the cart move left or right?"
    return prompt

def get_ai_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=10,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text.strip()

# API Key
#api_key = os.getenv("OPENAI_API_KEY")
#if not api_key:
#    raise ValueError("Please set the OPENAI_API_KEY environment variable")

openai.api_key = "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"

# Main
env_state = [0, 0, 0, 0]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        prompt = create_prompt(env_state)
        ai_response = get_ai_response(prompt)
        s.sendall(json.dumps({"text": ai_response}).encode('utf-8'))
        data = s.recv(1024)
        if data == b'done':
            break

print("GPT process has finished.")
