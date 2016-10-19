from ciscoconfparse import CiscoConfParse

config = CiscoConfParse("cisco_ipsec.txt")

group2s = config.find_objects_w_child(parentspec=r"^crypto map", childspec=r"^.*set pfs group2.*$")

print ""
print "Crypto Maps using PFS group 2:"
print "------------------------------"

for i in group2s:
    print i.text

print ""
