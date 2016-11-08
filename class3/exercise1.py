# This whole thing could probably get to be a bit cleaner and more scalable, but at a certain point it got to https://xkcd.com/1319/

import snmp_helper
import json
import sys
import smtplib
from email.mime.text import MIMEText


devices = [
    ('184.105.247.71','161'),
    ('184.105.247.70','161')
    ]

snmpuser = ('pysnmp','galileo1','galileo1')

oids = (
    ('Uptime','1.3.6.1.2.1.1.3.0'),
    ('RunningChanged','1.3.6.1.4.1.9.9.43.1.1.1.0'),
    ('RunningSaved','1.3.6.1.4.1.9.9.43.1.1.2.0'),
    ('StartupChanged','1.3.6.1.4.1.9.9.43.1.1.3.0')
    )

compiled_data = {} # a dictionary to hold the entire set of data (will be written to JSON at the end)
message = "" # a string to hold the message body of an email to be sent; if no devices changed, this will be blank

# try to load in the previous data from the .json file
try:
    with open("last_status.json") as f:
        existing_data = json.load(f)
        loaded_existing = True
except IOError:
    print "No previous data found"
    loaded_existing = False
except:
    print "Something went wrong, exiting"
    sys.exit()


# loop through the devices listed above
for device in devices:
    
    device_data = {} # this is a dictionary used to store the values for the current device only
    changes = [] # this is a list to track if any of the OIDs changed values for the current device only

    # loop through the list of OIDs to check
    for oid in oids:
        
        # acquire the current OID via SNMPv3 and extract just the value
        snmp_data = snmp_helper.snmp_extract(snmp_helper.snmp_get_oid_v3(device, snmpuser, oid[1]))
        
        # check to make sure already loaded the existing values, else we'll throw an error here
        if loaded_existing:

            # compare the old data to the new data to check for changes, but ignore the Uptime, since it'll always be different
            if (existing_data[device[0]][oid[0]] != snmp_data and oid[0] != 'Uptime'):
                changes.append({oid[0]:int(device_data['Uptime']) - int(snmp_data)})

        # if we didn't have existing values to load in, treat all the new stuff as a change (guarentee to send an email out)
        else:
            if (oid[0] != 'Uptime'):
                changes.append({oid[0]:int(device_data['Uptime']) - int(snmp_data)})

        # update the data for this device with the freshly polled value for this oid
        device_data.update({oid[0]:snmp_data})

    # loop through to detect any changes that occurred on this device since the last poll, and formulate a line in a string for each
    for change in changes:
        for key in change:
            m, s = divmod(change[key]/100, 60)
            h, m = divmod(m, 60)
            message += "Device " + device[0] + " had event " + key + " occur %d:%02d:%02d" % (h, m, s) + " ago.\n"

    # add the entire device data dictionary to the master dictionary
    compiled_data.update({device[0]:device_data})

# create a, or overwrite any existing, JSON file with our current timeticks for last changed and uptime
with open ("last_status.json", "w") as f:
   json.dump(compiled_data, f)

# if the message variable is blank, that means we accrued no changes; if it has value, something changes somewhere, and we need to send an email
# I know I could've imported email_helper.py, but I wanted to see how the actual commands you were using in that file worked, so i mostly just
# ripped it off here
if message != "":
    email_message = MIMEText(message)
    email_message['Subject'] = "Configuration Changes"
    email_message['From'] = "no-response@class3.pynet.org"
    email_message['To'] = "mele.chris@gmail.com"
    smtp_conn = smtplib.SMTP('localhost')
    smtp_conn.sendmail(email_message['From'], email_message['To'], email_message.as_string())
    smtp_conn.quit()
    print "Changes detected and email sent"
else:
    print "No changes detected"
