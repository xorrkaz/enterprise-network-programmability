#!/usr/bin/env python
#
# Copyright (c) 2017  Joe Clarke <jclarke@cisco.com>
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
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

# sys.path hack
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ncclient.manager import connect  # noqa

from tasks import constants  # noqa

ACL_CONFIG = '''
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ip>
      <access-list>
        <ios-acl:extended xmlns:ios-acl="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
          <ios-acl:name>WIN_ONLY</ios-acl:name>
          <ios-acl:access-list-seq-rule>
            <ios-acl:sequence>10</ios-acl:sequence>
              <ios-acl:ace-rule>
                <ios-acl:action>permit</ios-acl:action>
                <ios-acl:protocol>icmp</ios-acl:protocol>
                <ios-acl:host>198.18.133.36</ios-acl:host>
                <ios-acl:dst-host>{}</ios-acl:dst-host>
            </ios-acl:ace-rule>
          </ios-acl:access-list-seq-rule>
          <ios-acl:access-list-seq-rule>
            <ios-acl:sequence>20</ios-acl:sequence>
              <ios-acl:ace-rule>
                <ios-acl:action>deny</ios-acl:action>
                <ios-acl:protocol>icmp</ios-acl:protocol>
                <ios-acl:any/>
                <ios-acl:dst-host>{}</ios-acl:dst-host>
            </ios-acl:ace-rule>
          </ios-acl:access-list-seq-rule>
          <ios-acl:access-list-seq-rule>
            <ios-acl:sequence>30</ios-acl:sequence>
              <ios-acl:ace-rule>
                <ios-acl:action>permit</ios-acl:action>
                <ios-acl:protocol>ip</ios-acl:protocol>
                <ios-acl:any/>
                <ios-acl:dst-any/>
            </ios-acl:ace-rule>
          </ios-acl:access-list-seq-rule>
        </ios-acl:extended>
      </access-list>
    </ip>
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <ip>
          <access-group>
            <in>
              <acl>
                <acl-name>WIN_ONLY</acl-name>
                <in/>
              </acl>
            </in>
          </access-group>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
</config>
'''.format(constants.CSR_HOST, constants.CSR_HOST)


def configure_acl():
    connection_params = {
        'host': constants.CSR_HOST,
        'username': constants.CSR_USERNAME,
        'password': constants.CSR_PASSWORD,
        'hostkey_verify': False,
        'device_params': {'name': 'csr'}
    }
    with connect(**connection_params) as m:
        try:
            m.edit_config(target='running', config=ACL_CONFIG)
            print('Successfully configured ACL on {}'.format(constants.CSR_HOST))
        except Exception as e:
            print('Failed to configure ACL: {}'.format(e))


def main():
    configure_acl()


if __name__ == '__main__':
    main()
