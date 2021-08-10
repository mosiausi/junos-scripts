# bgp-peer-count.py
# Aug 10 2021
# Version 1.0
# Moshiko Nayman - mosiausi@gmail.com
# BGP peer count to monitor the BGP peer scale on BGP allow (unconfigured-peers)

#!/usr/bin/python
import jcs
from jnpr.junos import Device
from junos import Junos_Context


def main():
    jcs.syslog('external.notice', 'BGP Script Started')
    dev = Device()

    dev.open()
    result = dev.rpc.get_bgp_summary_information()
    peer_count = result.findtext('peer-count')

    snmp_set = \
        dev.rpc.request_snmp_utility_mib_set(object_type='counter64',
            instance='bgp_peer_count', object_value=peer_count)
    snmp_result = snmp_set.findtext('snmp-utility-mib-result')

    jcs.syslog('external.notice', snmp_result)
    jcs.syslog('external.notice', 'BGP Script Ended')

    dev.close()


if __name__ == '__main__':
    main()

# set event-options generate-event 1-MIN time-interval 60
# set event-options policy BGP-PEER-COUNT events 1-MIN
# set event-options policy BGP-PEER-COUNT then event-script bgp-peer-count.py
# set event-options event-script file bgp-peer-count.py
# root@vMX-R1> show snmp mib walk jnxUtil 
# jnxUtilCounter64Value.98.103.112.95.112.101.101.114.95.99.111.117.110.116 = 1024
