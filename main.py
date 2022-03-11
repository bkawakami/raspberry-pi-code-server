from fabric import Connection, Config

import getpass

host = input("Host: ")

port = input("Port: ")

user = input("Username: ")

user_pass = getpass.getpass("Password: ")

config = Config(overrides={'sudo': {'password': user_pass}})

c = Connection('%s@%s:%s' % (user, host, port), connect_kwargs={"password": user_pass}, config=config)



c.run('sudo apt update', pty=True)
c.run('sudo apt install curl -y', pty=True)
c.run('sudo apt install supervisor -y', pty=True)
c.run('sudo curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -', pty=True)
c.run('sudo apt update', pty=True)
c.run('sudo apt install nodejs -y', pty=True)
c.run('curl https://get.telebit.io/ | bash', pty=True)
c.run('/home/ubuntu/telebit list', pty=True)
telebit_domain = input("Put your Telebit Domain: ")
c.run('wget https://code-server.dev/install.sh', pty=True)
c.run('sudo sh install.sh', pty=True)
c.put('files/codeserver.conf', '/etc/supervisor/conf.d/codeserver.conf', pty=True)
c.run('sudo systemctl reload supervisor', pty=True)
c.run('sudo systemctl restart supervisor', pty=True)
c.run('/home/ubuntu/telebit http 8080 code', pty=True)
