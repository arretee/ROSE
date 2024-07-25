import os
import signal
import sys
import subprocess

def main():
    file = open("settings.txt").readlines()
    venv_active = file[0][16:]



def start_server(venv_active, path, params):
    os.chdir(r"C:\AeroData\NitzanimFiles\RedHatProject\Rose")
    a = subprocess.run(
        r'cmd /c ".venv\rose\Scripts\activate && echo Activation successful && set"',
        cwd=r"C:\AeroData\NitzanimFiles\RedHatProject",
        capture_output=True,
        text=True,
        shell=True
    )
    print(a)
    os.chdir(r"C:\AeroData\NitzanimFiles\RedHatProject\Rose")
    server = subprocess.Popen(args=['python', "rose-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    input("eeeee: ")
    os.kill(server.pid, signal.SIGINT)



def start_client(venv_active, path, params):
    pass


if __name__ == '__main__':
    file = open("settings.txt").readlines()

    start_server(file[0][16:], file[1][16:], file[2][16:])
