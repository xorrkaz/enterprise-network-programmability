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

from ncclient import manager

acl_cfg = '''
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ip>
      <access-list>
        <ios-acl:standard xmlns:ios-acl="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
          <ios-acl:name>WIN_ONLY</ios-acl:name>
          <ios-acl:access-list-seq-rule>
            <ios-acl:sequence>10</ios-acl:sequence>
            <ios-acl:permit>
              <ios-acl:std-ace>
                <ios-acl:host>198.18.133.36</ios-acl:host>
              </ios-acl:std-ace>
            </ios-acl:permit>
          </ios-acl:access-list-seq-rule>
          <ios-acl:access-list-seq-rule>
            <ios-acl:sequence>20</ios-acl:sequence>
            <ios-acl:deny>
              <ios-acl:std-ace>
                <ios-acl:any/>
              </ios-acl:std-ace>
            </ios-acl:deny>
          </ios-acl:access-list-seq-rule>
        </ios-acl:standard>
      </access-list>
    </ip>
    <interface>
      <GigabitEthernet>
        <name>2</name>
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
'''

with manager.connect_ssh(host='198.18.133.212', port=830, username='admin', hostkey_verify=False, password='C1sco12345') as m:
    try:
        m.edit_config(target='running', config=acl_cfg)
        print('Successfully configured ACL on {}'.format(RTR_IP))
    except Exception as e:
        print('Failed to configre ACL: {}'.format(e))
