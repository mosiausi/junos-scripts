#! /usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import jcs
import sys

def main():

    usage = """
        # Moshiko Nayman script #
        This script sets description to the specified interface.
        The script modifies the candidate configuration to a new
        description and commits the configuration to activate it.
    """
    print (usage)

    description = jcs.get_input("Enter description to lo0: ")
    if not description:
       print ("invalid description")
       sys.exit(1)

    config_xml = """
        <configuration>
            <interfaces>
                <interface>
                    <name>lo0</name>
                    <unit>
                        <name>0</name>
                        <description>{0}</description>
                    </unit>
                </interface>
            </interfaces>
        </configuration>
    """.format(description).strip()

    dev = Device()
    dev.open()
    try:
        with Config(dev, mode="exclusive") as cu:
            print ("Loading and committing configuration changes")
            cu.load(config_xml, format="xml", merge=True)
            cu.commit()

    except Exception as err:
        print (err)
        dev.close()
        return

    dev.close()

if __name__ == "__main__":
    main()
