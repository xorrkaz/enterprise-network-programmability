#!/usr/bin/env python
# ############################################################################
# Copyright (c) 2016-2018 Bruno Klauser, Joe Clarke, Dmitry Figol
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ''AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#
# TECHNICAL ASSISTANCE CENTER (TAC) SUPPORT IS NOT AVAILABLE FOR THIS SCRIPT.
#


"""This sample script illustrates how to query operational data from a router
via the RESTCONF API and then post the results into an existing Spark room
via the Spark REST APIs.
"""
# sys.path hack
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests  # noqa

from tasks import constants, env, helper  # noqa


INTERFACE_NAME = 'GigabitEthernet1'
INTERFACE_STATS_ENDPOINT = '/data/interfaces-state/interface'
HOSTNAME_ENDPOINT = '/data/native/hostname'

SPARK_MESSAGE_TEMPLATE = ('Interface **{interface_name}** on the device **{hostname}** '
                          'has received **{in_octets} bytes** '
                          'and transmitted **{out_octets} bytes.**')


def get_hostname():
    response = requests.get(
        '{}{}'.format(constants.RESTCONF_ROOT, HOSTNAME_ENDPOINT),
        headers=constants.RESTCONF_HEADERS,
        auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD),
        verify=False
    )
    response.raise_for_status()

    return response.json()['Cisco-IOS-XE-native:hostname']


def get_interface_statistics(interface_name, hostname):
    response = requests.get(
        '{}{}={}'.format(constants.RESTCONF_ROOT, INTERFACE_STATS_ENDPOINT, interface_name),
        headers=constants.RESTCONF_HEADERS,
        auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD),
        verify=False
    )
    response.raise_for_status()

    interface_stats = response.json()['ietf-interfaces:interface'].get('statistics', {})
    in_octets = interface_stats.get('in-octets')
    out_octets = interface_stats.get('out-octets')
    if in_octets is None or out_octets is None:
        print('Interface {} does not have traffic statistics')
    else:
        spark_message = SPARK_MESSAGE_TEMPLATE.format(
            session_name=env.LAB_SESSION, user=env.LAB_USER,
            interface_name=interface_name, hostname=hostname,
            in_octets=in_octets, out_octets=out_octets
        )
        helper.send_spark_message(markdown=spark_message)


def main():
    # Disable warnings for self-signed certificate
    requests.packages.urllib3.disable_warnings()

    hostname = get_hostname()
    get_interface_statistics(INTERFACE_NAME, hostname)


if __name__ == '__main__':
    main()
