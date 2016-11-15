import paramiko
from time import sleep

host = '184.105.247.71'
username = 'pyclass'
password = '88newclass'

# a function to just clean up some sending/receiving
def send(ssh_connection, command):
    ssh_connection.send(command + "\n")
    sleep(2)
    output = ""
    while ssh_connection.recv_ready():
        output += ssh_connection.recv(65535)
    return output

# start up our connection to rtr2
connect = paramiko.SSHClient()

# automatically accept whatever the key is for the remote host
connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())

connect.connect(host, username=username, password=password, look_for_keys=False, allow_agent=False)

rtr2 = connect.invoke_shell()

output = rtr2.recv(5000)

print send(rtr2, "terminal length 0")
print send(rtr2, "show version")
