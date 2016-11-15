import netmiko

devices = [
    {'device_type': 'cisco_ios', 'ip': '184.105.247.70', 'username': 'pyclass', 'password': '88newclass'},
    {'device_type': 'cisco_ios', 'ip': '184.105.247.71', 'username': 'pyclass', 'password': '88newclass'},
    {'device_type': 'juniper', 'ip': '184.105.247.76', 'username': 'pyclass', 'password': '88newclass'}
]   

for device in devices:
    connect = netmiko.ConnectHandler(**device)

    # print out the prompt so the user can see we're on the correct device
    print connect.find_prompt()

    # print the result of the 'show arp' command - this only works b/c the command is the same on IOS and JUNOS
    print connect.send_command('show arp')
