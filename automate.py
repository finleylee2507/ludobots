import subprocess

for i in range(1, 6):
    command = f'python search.py {i}'
    subprocess.run(command.split())