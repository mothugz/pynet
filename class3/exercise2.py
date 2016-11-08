# Ok, I know this is kind of a mess, but I did a lot of messing around and learning on this, and in the end I can definitely figure out a way to
# clean up this programming and do it in a lot fewer lines and probably less resources.. Mostly this was a "one thing leads to another leads to
# another" type of script, and suddenly it's kind of ugly. However, it seems to fulfill its requirements, and I definitely learned a lot about
# Python creating it.

import snmp_helper
import pygal
import time

DELAY = 300 # the delay between polls in seconds)

device = ('184.105.247.70','161')
snmpuser = ('pysnmp','galileo1','galileo1')

iterator = [] # a list we'll keep our timestamps in
ifInOctets_fa4_raw = [] # a list we'll keep our bytes in on Fa4
ifInUcastPkts_fa4_raw = [] # a list we'll keep our packets in on Fa4
ifOutOctets_fa4_raw = [] # a list we'll keep our bytes out on Fa4
ifOutUcastPkts_fa4_raw = [] # a list we'll keep our packets out on Fa4
ifInOctets_fa4_rate = [] # a list we'll keep the delta bytes in on Fa4
ifInUcastPkts_fa4_rate = [] # a list we'll keep the delta packets in on Fa4
ifOutOctets_fa4_rate = [] # a list we'll keep the delta bytes out on Fa4
ifOutUcastPkts_fa4_rate = [] # a list we'll keep the delta packets out on Fa4


our_epoch = time.time() # get our start time

# yea, i know, if the interface changes its description over time, this won't pick it up
graph_title = snmp_helper.snmp_extract(snmp_helper.snmp_get_oid_v3(device, snmpuser, '1.3.6.1.2.1.2.2.1.2.5'))

# i know this should be a for loop if we only want to go 10 times, but in theory i'd like to continuously poll the network at a regular interval
while True:
    # iterator will be our X-axis - maybe I'll change this to timestamp
    iterator.append(time.time()-our_epoch)
    #print iterator # debug print

    # store the raw output of the packets and octets in these arrays - this would be akin to a poller that then writes the values to a database
    ifInOctets_fa4_raw.append(snmp_helper.snmp_extract(snmp_helper.snmp_get_oid_v3(device, snmpuser, '1.3.6.1.2.1.2.2.1.10.5')))
    ifInUcastPkts_fa4_raw.append(snmp_helper.snmp_extract(snmp_helper.snmp_get_oid_v3(device, snmpuser, '1.3.6.1.2.1.2.2.1.11.5')))
    ifOutOctets_fa4_raw.append(snmp_helper.snmp_extract(snmp_helper.snmp_get_oid_v3(device, snmpuser, '1.3.6.1.2.1.2.2.1.16.5')))
    ifOutUcastPkts_fa4_raw.append(snmp_helper.snmp_extract(snmp_helper.snmp_get_oid_v3(device, snmpuser, '1.3.6.1.2.1.2.2.1.17.5')))

    # we only want to do math if there's actually math to do (on the first pass, we won't get a difference in counts)
    if len(iterator) > 1:            

            # calculate and store the difference between the current poll and the last poll here        
            ifInOctets_fa4_rate.append(int(ifInOctets_fa4_raw[len(iterator)-1]) - int(ifInOctets_fa4_raw[len(iterator)-2]))
            ifInUcastPkts_fa4_rate.append(int(ifInUcastPkts_fa4_raw[len(iterator)-1]) - int(ifInUcastPkts_fa4_raw[len(iterator)-2]))
            ifOutOctets_fa4_rate.append(int(ifOutOctets_fa4_raw[len(iterator)-1]) - int(ifOutOctets_fa4_raw[len(iterator)-2]))
            ifOutUcastPkts_fa4_rate.append(int(ifOutUcastPkts_fa4_raw[len(iterator)-1]) - int(ifOutUcastPkts_fa4_raw[len(iterator)-2]))

            # debug prints
            #print ifInOctets_fa4_rate
            #print ifInUcastPkts_fa4_rate
            #print ifOutOctets_fa4_rate
            #print ifOutUcastPkts_fa4_rate

            x_axis = [] # an array to hold the x-axis labels

            for j in range(1,len(iterator)):
                x_axis.append(time.strftime('%H:%M:%S', time.localtime(our_epoch+iterator[j])))

            #x_axis = iterator[1:] # did this to get rid of the first label on the x_axis, since there's no good way to start that very first data point off. I tried, but couldn't get the iterator.pop(0) command to work as I wanted it to.
            #print x_axis

            packets_chart = pygal.Line()
            packets_chart.title = "Input/Output Packets :: Fa4 :: " + graph_title
            packets_chart.x_labels = x_axis
            packets_chart.add("InPackets", ifInUcastPkts_fa4_rate)
            packets_chart.add("OutPackets", ifOutUcastPkts_fa4_rate)

            octets_chart = pygal.Line()
            octets_chart.title = "Input/Output Bytes :: Fa4 :: " + graph_title
            octets_chart.x_labels = x_axis
            octets_chart.add("InBitrate", ifInOctets_fa4_rate)
            octets_chart.add("OutBitrate", ifOutOctets_fa4_rate)
 
            packets_chart.render_to_file("packets_chart.svg")
            octets_chart.render_to_file("octets_chart.svg")
    # do the time delay this way in order to compensate for drift due to polling and processing latency
    time.sleep(DELAY - ((time.time() - our_epoch) - iterator[len(iterator)-1]))
