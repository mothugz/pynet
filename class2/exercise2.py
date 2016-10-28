import telnetlib
import time

ip_addr = '184.105.247.70'
TELNET_PORT = '23'
TELNET_TIMEOUT = 6

remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
remote_conn.read_until("sername:", TELNET_TIMEOUT)
remote_conn.write("pyclass" + '\n')
remote_conn.read_until("assword:", TELNET_TIMEOUT)
remote_conn.write("88newclass" + '\n')
remote_conn.read_until("#", TELNET_TIMEOUT)
remote_conn.write("show ip interface brief" + '\n')
time.sleep(2)
print remote_conn.read_very_eager()
remote_conn.close()

