import netmiko

rtr2 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.71',
    'username': 'pyclass',
    'password': '88newclass'
}

connect = netmiko.ConnectHandler(**rtr2)

# print out the prompt so the user can see we're on the correct device
print connect.find_prompt()

# enter the configuration mode on the router
connect.config_mode()

# print out the prompt again so the user can we've successfully entered config mode
print connect.find_prompt()

# the boolean that netmiko returns to verify config mode was successfully entered
print connect.check_config_mode()
