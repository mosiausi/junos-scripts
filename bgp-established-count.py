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
    established_count = result.findtext('bgp-group/established-count')

    snmp_set = \
        dev.rpc.request_snmp_utility_mib_set(object_type='counter64',
            instance='bgp_established_count', object_value=established_count)
    snmp_result = snmp_set.findtext('snmp-utility-mib-result')

    jcs.syslog('external.notice', snmp_result)
    jcs.syslog('external.notice', 'BGP Script Ended')

    dev.close()


if __name__ == '__main__':
    main()

# set event-options generate-event 1-MIN time-interval 60
# set event-options policy BGP-ESTABLISHED-COUNT events 1-MIN
# set event-options policy BGP-ESTABLISHED-COUNT then event-script bgp-established-count.py
# set event-options event-script file bgp-established-count.py

