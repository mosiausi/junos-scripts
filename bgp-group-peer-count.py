#!/usr/bin/python

import jcs
from jnpr.junos import Device
from junos import Junos_Context


def main():
    jcs.syslog('external.notice', 'BGP Script Started')
    dev = Device()

    # dev = Device(host="66.129.235.2" , port=22 , user="jcluser" , password="Juniper!1"

    dev.open()
    result = dev.rpc.get_bgp_group_information(summary=True)
    peer_count = result.findtext('bgp-group/peer-count')

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
# set event-options policy BGP-GROUP-PEER-COUNT events 1-MIN
# set event-options policy BGP-GROUP-PEER-COUNT then event-script bgp-group-peer-count.py
# set event-options event-script file bgp-group-peer-count.py
