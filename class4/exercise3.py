import pexpect

host = '184.105.247.71'
username = 'pyclass'
password = '88newclass'


def send(ssh_connection, command, expect):
    ssh_connection.sendline(command)
    ssh_connection.expect(prompt)

ssh_connection = pexpect.spawn('ssh -l {} {}'.format(username, host))
ssh_connection.timeout = 3
ssh_connection.expect('assword:')

ssh_connection.sendline(password)
ssh_connection.expect('#')

prompt = ssh_connection.before.strip() + ssh_connection.after

send(ssh_connection, 'terminal length 0', prompt)
send(ssh_connection, 'show ip interface brief', prompt)
print ssh_connection.before
