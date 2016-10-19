from ciscoconfparse import CiscoConfParse

config = CiscoConfParse("cisco_ipsec.txt")

aes = config.find_objects_wo_child(parentspec=r"^crypto map", childspec=r"^.*set transform-set.*AES.*$")

print ""
print "Crypto Maps not using AES encryption (based on name of policy):"
print "---------------------------------------------------------------"
for i in aes:
    print i.text

print ""
