from fabric import Connection, Config

import getpass

import time

import re

from rich.progress import Progress
from rich.prompt import Prompt
from rich import print
from rich.panel import Panel


import pyfiglet
  
result = pyfiglet.figlet_format("Auto Build K", font='big')
print(result)


print(Panel("Insert information", style="on blue"))

host = Prompt.ask("Enter the host domain or IP", default="localhost")

port = Prompt.ask("SSH Port", default="22")

user = Prompt.ask("SSH User connection", default="ubuntu")

user_pass = Prompt.ask("SSH User password", password=True)


with Progress() as progress:    

    task1 = progress.add_task("[green]Get data...", total=1000)

    progress.update(task1, advance=200)

    config = Config(overrides={'sudo': {'password': user_pass}})

    c = Connection('%s@%s:%s' % (user, host, port), connect_kwargs={"password": user_pass}, config=config)


    print(Panel("Getting system info...", style="on green"))
    distro_os = c.run('lsb_release -a')

    progress.update(task1, advance=400)


    arch = c.run('file /lib/systemd/systemd')

    progress.update(task1, advance=400)



    distro_info = distro_os.stdout.strip().splitlines()[1].lower()
    distro_version = re.findall(r'\d+', distro_info)

    if "ubuntu" not in distro_info:
        print(Panel("Distro not supported", style="on red"))
        exit()
    else:
        if int(distro_version[0]) >= 20:
            print(Panel("Distro supported", style="on green"))
        else:
            print(Panel("Distro not supported", style="on red"))
            exit()


    task2 = progress.add_task("[cyan]Installing...", total=1000)

    print(Panel("Installing dependencies...", style="on green"))

    progress.update(task2, advance=20)

    c.run('sudo apt update')

    progress.update(task2, advance=30)

    c.run('sudo apt autoremove -y')

    progress.update(task2, advance=50)

    c.run('sudo apt install curl wget python3-pip -y')
    c.run('sudo apt install supervisor -y')

    progress.update(task2, advance=200)

    if "32-bit" not in arch.stdout.strip():
        c.run('sudo snap install ngrok')
        auth_ngrok = Prompt.ask("Ngrok Auth Token:", password=True)
        c.run('ngrok authtoken %s' % (auth_ngrok))
        c.run('sudo curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -')
        c.run('sudo apt update')
        c.run('sudo apt install nodejs -y')
        c.run('wget https://code-server.dev/install.sh')
        c.run('sudo sh install.sh')
        c.put('files/codeserver.conf', remote='/home/%s/codeserver.conf' % user)
        c.run('sudo mv /home/%s/codeserver.conf /etc/supervisor/conf.d/codeserver.conf' % user)
        c.put('./files/ngrok-code.conf', remote='/home/%s/ngrok-code.conf' % user)
        c.run('sudo mv /home/%s/ngrok-code.conf /etc/supervisor/conf.d/ngrok-code.conf' % user)
        progress.update(task2, advance=300)
    else:
        print(Panel("Code server is not compatible with 32-bit architecture", style="on orange3"))
        progress.update(task2, advance=300)
        
    c.run('sudo pip3 install schedule')
    c.put('./files/schedulers.conf', remote='/home/%s/schedulers.conf' % user)
    c.run('sudo mv /home/%s/schedulers.conf /etc/supervisor/conf.d/schedulers.conf' % user)

    progress.update(task2, advance=100)

    c.run('mkdir -p /home/%s/Projects/Schedulers' % user)
    c.put('./files/pi_schedule.py', remote='/home/%s/Projects/Schedulers/pi_schedule.py' % user)

    progress.update(task2, advance=100)

    c.run('sudo systemctl reload supervisor')
    c.run('sudo systemctl restart supervisor')
    time.sleep(10)
    progress.update(task2, advance=200)

print(Panel("Done", style="on green"))
