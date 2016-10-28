from exercise3 import IOSTelnet
import sys

c = IOSTelnet("184.105.247.70", "pyclass", "88newclass")
error = c.telnet_connect()
if error == -1:
    sys.exit("Connection timed out")

print c.login(),
print c.disable_paging(),
print c.send_command("sh ip int brief"),

