# prompt-control
ChatGPT for dynamic system control planning, supporting openAI Gym, Docker, EnergyPlus, etc,

# Setup
Need X11 session to render.

# Example

- go to `gpt_gym`
- open a terminal, and start the gym environment server by running `python gym_server.py`. The default game is "CartPole-v1".
- open another terminal, and start the GPT interface by `python gpt_interface.py`.
- then you can control the env by simply tell the GPT to move the cart pole to left or right. It will automatically generate code to execute that command.

# TODOs
- enable video record
- support docker app, such as containerized energyplus or modelica
