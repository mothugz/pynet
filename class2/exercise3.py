import telnetlib
import time
import socket

TIMEOUT = 6

class IOSTelnet(object):

    def __init__(self, host, username, password, port=23):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def login(self):
        output = self.connection.read_until("sername:", TIMEOUT)
        self.connection.write(self.username + '\n')
        output += self.connection.read_until("assword:", TIMEOUT)
        self.connection.write(self.password + '\n')
        output += self.connection.read_until("#", TIMEOUT)
        self.prompt = output.split("\n")[-1]
        return output

    def disable_paging(self):
        return self.send_command("term len 0")

    def send_command(self, command):
        command = command.rstrip()
        self.connection.write(command + "\n")
        return self.connection.read_until(self.prompt, TIMEOUT)

    def telnet_connect(self):
        try:
            self.connection = telnetlib.Telnet(self.host, self.port, TIMEOUT)
        except socket.timeout:
            return -1

    def disconnect(self):
        self.connection.close() 
