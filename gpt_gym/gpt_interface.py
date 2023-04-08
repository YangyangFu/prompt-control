import openai
import re
import argparse
import math
import numpy as np
import os
import json
import time

from agents import RandomDiscreteAgent
from gym_client import ClientWrapper

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, default="prompts/basic.txt")
parser.add_argument("--sysprompt", type=str,
                    default="prompts/system.txt")
args = parser.parse_args()

# get openai api key
api_key = os.getenv("OPENAI_API_KEY")
print("Initializing ChatGPT...")
openai.api_key = api_key

with open(args.sysprompt, "r") as f:
    sysprompt = f.read()

chat_history = [
    {
        "role": "system",
        "content": sysprompt
    },
    {
        "role": "user",
        "content": "move left"
    },
    {
        "role": "assistant",
        "content": """```python
gc.step(0)
```
This code uses the `step()` function to move the cart pole to left from the current position. It does this by setting the action to 0`."""
    }
]


def ask(prompt):
    chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0
    )
    chat_history.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content,
        }
    )
    return chat_history[-1]["content"]


print(f"Done.")

code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)


def extract_python_code(content):
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None


class colors:  # You may need to change color settings
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


print(f"Initializing gym client...")
remote_base = 'http://127.0.0.1:5000'
gc = ClientWrapper(remote_base)
print(f"Done.")

print(f"Initializing control agent...")
ag = RandomDiscreteAgent(2)
print(f"Done.")

with open(args.prompt, "r") as f:
    prompt = f.read()

ask(prompt)
print("Welcome to the Gym chatbot! I am ready to help you with your questions and commands.")

while True:
    question = input(colors.YELLOW + "Gym Control> " + colors.ENDC)

    if question == "!quit" or question == "!exit":
        break

    if question == "!clear":
        os.system("cls")
        continue

    response = ask(question)

    print(f"\n{response}\n")

    code = extract_python_code(response)
    if code is not None:
        print("Please wait while I run the code in Gym ClientWrapper...")
        exec(extract_python_code(response))
        print("Done!\n")
