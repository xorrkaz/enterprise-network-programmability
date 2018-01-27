#!/usr/bin/env python
# ############################################################################
# Copyright (c) 2018 Dmitry Figol, Cisco Systems
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
# ############################################################################

import re
import requests

# sys.path hack
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tasks import constants, helper  # noqa

EXTENDED_ACL_ENDPOINT = '/data/native/ip/access-list/extended'
INTERFACE_ENDPOINT = '/data/native/interface/'
INTERFACE_ACL_ENDPOINT = '/data/native/interface/{interface_type}={interface_number}/ip/access-group/{direction}/acl'

INTERFACE_TO_APPLY = 'GigabitEthernet1'
ACL_DIRECTION = 'in'
EXTENDED_ACL_NAME = 'WIN_ONLY'

ACL_JSON = {
    "extended": [
        {
            "name": "WIN_ONLY",
            "access-list-seq-rule": [
                {
                    "sequence": 10,
                    "ace-rule": {
                        "action": "permit",
                        "protocol": "icmp",
                        "host": constants.WINDOWS_WORKSTATION,
                        "dst-host": constants.CSR_HOST
                    }
                },
                {
                    "sequence": 20,
                    "ace-rule": {
                        "action": "deny",
                        "protocol": "icmp",
                        "any": [
                            None
                        ],
                        "dst-host": constants.CSR_HOST
                    }
                },
                {
                    "sequence": 30,
                    "ace-rule": {
                        "action": "permit",
                        "protocol": "ip",
                        "any": [
                            None
                        ],
                        "dst-any": [
                            None
                        ]
                    }
                }
            ]
        }
    ]
}


INTERFACE_NAME_RE = re.compile(r'(?P<interface_type>[a-zA-Z\-]+)(?P<interface_number>[\d/.]+)')


def remove_acl_if_exists(extended_acl_name):
    """Checks if ACL with the specified name already exists and removes it

    Args:
        extended_acl_name (str): name of the ACL to check

    Returns:
        None
    """
    # Check if ACL exists
    # GET https://198.18.133.212/restconf/data/native/ip/access-list/extended=WIN_ONLY
    response = requests.get(
        '{}{}={}'.format(constants.RESTCONF_ROOT, EXTENDED_ACL_ENDPOINT, extended_acl_name),
        headers=constants.RESTCONF_HEADERS, auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD), verify=False
    )

    if response.ok:
        print('Extended ACL {} already exists, removing'.format(extended_acl_name))
        response = requests.delete(
            '{}{}={}'.format(constants.RESTCONF_ROOT, EXTENDED_ACL_ENDPOINT, extended_acl_name),
            headers=constants.RESTCONF_HEADERS, auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD), verify=False
        )
        if response.ok:
            print('Extended ACL {} was successfully deleted'.format(extended_acl_name))
        else:
            print('Unexpected: status code is {} instead of 204 - no content'.format(response.status_code))


def remove_acl_from_interface(interface_name, direction):
    """Checks if ACL is applied on the interface in specified direction and removes it

    Args:
        interface_name (str): name of the interface where ACLs should be checked
        direction (str): direction in which ACL should be checked. One of ['in', 'out']

    Returns:
        None
    """
    # Check if any ACL is applied on the interface
    # GET https://198.18.133.212/restconf/data/native/interface/GigabitEthernet=2/ip/access-group/in/acl
    parsed_interface_name = INTERFACE_NAME_RE.match(interface_name).groupdict()
    response = requests.get(
        constants.RESTCONF_ROOT + INTERFACE_ACL_ENDPOINT.format(direction=direction, **parsed_interface_name),
        headers=constants.RESTCONF_HEADERS, auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD), verify=False
    )

    if response.ok:
        acl_name = response.json()['Cisco-IOS-XE-native:acl']['acl-name']
        print('ACL {} is currently applied on the interface {} in "{}" direction'.format(
            acl_name, interface_name, direction.upper()
        ))
        response = requests.delete(
            constants.RESTCONF_ROOT + INTERFACE_ACL_ENDPOINT.format(direction=direction, **parsed_interface_name),
            headers=constants.RESTCONF_HEADERS, auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD), verify=False
        )

        if response.ok:
            print('ACL {} was successfully removed from the interface {} in "{}" direction'.format(
                acl_name, interface_name, direction.upper()
            ))
        else:
            print('Unexpected: status code is {} instead of 204 - no content'.format(response.status_code))


def configure_acl(acl):
    """Configure ACL using RESTCONF

    Args:
        acl (dict): JSON-like dictionary representing access-list with YANG in JSON format

    Returns:
        None
    """
    # PUT https://198.18.133.212/restconf/data/native/ip/access-list/extended=WIN_ONLY
    extended_acl_name = acl['extended'][0]['name']

    response = requests.put(
        '{}{}={}'.format(constants.RESTCONF_ROOT, EXTENDED_ACL_ENDPOINT, extended_acl_name),
        json=acl, headers=constants.RESTCONF_HEADERS,
        auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD), verify=False
    )

    if response.ok:
        print('Successfully configured extended ACL {}'.format(extended_acl_name))
    else:
        print('Unexpected: status code is {} instead of 204 - no content'.format(response.status_code))


def apply_acl(interface_name, direction, acl_name):
    """Applies ACL to the interface in specified direction using RESTCONF.

    Args:
        interface_name (str): name of the interface. For example, GigabitEthernet2
        direction (str): direction in which ACL should be applied. One of ['in', 'out']
        acl_name (str): name of ACL that should be applied

    Returns:
        None
    """
    # PUT https://198.18.133.212/restconf/data/native/interface/GigabitEthernet=2/ip/access-group/in/acl
    parsed_interface_name = INTERFACE_NAME_RE.match(interface_name).groupdict()

    interface_acl_json = {
        "acl": {
            "acl-name": acl_name,
            direction: [
                None
            ]
        }
    }

    response = requests.put(
        constants.RESTCONF_ROOT + INTERFACE_ACL_ENDPOINT.format(direction=direction, **parsed_interface_name),
        json=interface_acl_json,
        headers=constants.RESTCONF_HEADERS, auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD), verify=False
    )

    if response.ok:
        print('ACL {} was successfully applied on the interface {} in "{}" direction'.format(
            acl_name, interface_name, direction.upper()
        ))
    else:
        print('Unexpected: response status code is {}'.format(response.status_code))


def main():
    # Disable warnings for self-signed certificate
    requests.packages.urllib3.disable_warnings()

    # Check that RESTCONF service is running
    helper.check_restconf()

    acl_name = ACL_JSON['extended'][0]['name']

    remove_acl_if_exists(acl_name)
    remove_acl_from_interface(INTERFACE_TO_APPLY, ACL_DIRECTION)
    configure_acl(ACL_JSON)
    apply_acl(INTERFACE_TO_APPLY, ACL_DIRECTION, acl_name)


if __name__ == '__main__':
    main()
