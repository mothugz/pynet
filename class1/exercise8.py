from ciscoconfparse import CiscoConfParse

config = CiscoConfParse("cisco_ipsec.txt")

crypto = config.find_objects(r"^crypto map")

for i in crypto:
    print i.text
    for j in i.all_children:
        print j.text

