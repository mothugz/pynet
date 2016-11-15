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

# changed the log buffer size
connect.send_command('logging buffered 8092')

# exit config mode
connect.exit_config_mode()

# find the log buffer size in the config to verify the command worked
print connect.send_command('show run | i logging buffered')
