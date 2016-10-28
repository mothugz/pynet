import snmp_helper

COMMUNITY = "galileo"
SNMP_PORT = "161"

def snmpget(host, oid):
    return snmp_helper.snmp_extract(snmp_helper.snmp_get_oid((host, COMMUNITY, SNMP_PORT), oid))

hosts_to_query = ["184.105.247.70", "184.105.247.71"]

for host in hosts_to_query:
    print snmpget(host, "1.3.6.1.2.1.1.5.0")
    print snmpget(host, "1.3.6.1.2.1.1.1.0")
    print ""


   
