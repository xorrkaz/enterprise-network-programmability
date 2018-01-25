#!/usr/bin/env python
# ############################################################################
# Copyright (c) 2018 Bruno Klauser <bklauser@cisco.com>, Dmitry Figol
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
# ############################################################################
# 
# This is a simple hello lab script (will create the spark room if needed) 
# 
# ############################################################################
import _LabEnv
import requests
import sys
# Disable Certificate warning
requests.packages.urllib3.disable_warnings()


# ############################################################################
# Variables below
# ############################################################################
SPARK_ROOM_ID = None
CHECK_MARK_SYMBOL = u'\u2705'
CROSS_MARK_SYMBOL = u'\u274C'
APIC_EM_AUTH_ENDPOINT = '/ticket'

# ############################################################################
# Find (or Create) Spark Room
# ############################################################################
response = requests.get(_LabEnv.SPARK_API_ROOMS, headers=_LabEnv.SPARK_HEADERS, verify=False)

for tmproom in response.json()['items']:
    if tmproom['title'] == _LabEnv.SPARK_ROOM_NAME:
        SPARK_ROOM_ID = tmproom['id']
        # print("Found room ID for '{}' : {}".format(_LabEnv.SPARK_ROOM_NAME, SPARK_ROOM_ID))
        break
    
if SPARK_ROOM_ID is None:
    print("Failed to find room ID for '{}' creating it ...".format(_LabEnv.SPARK_ROOM_NAME))
    print("It seems that you are not in the joint spark room when the script was run, "
          "please let the proctor know")
    data = {'title': _LabEnv.SPARK_ROOM_NAME}
    # print('Spark Request: ' + t)
    response = requests.post(_LabEnv.SPARK_API_ROOMS, json=data,
                             headers=_LabEnv.SPARK_HEADERS, verify=False)
    # print('Spark Response: ' + r.text)
    SPARK_ROOM_ID = response.json()['id']

if SPARK_ROOM_ID is None:
    print("Failed to find or create room ID for '" + _LabEnv.SPARK_ROOM_NAME + "'")
    sys.exit(1)

# ############################################################################
# Verify Lab Environment
# ############################################################################

# Python Version and Platform info
lab_state = u'{} Python ({} on {})\n'.format(CHECK_MARK_SYMBOL, sys.version, sys.platform)

# Spark Room info
lab_state += u'{} Spark Room (ID={})\n'.format(CHECK_MARK_SYMBOL, SPARK_ROOM_ID)

# dCloud Session info
# TBD once session.xml is provisioned
dCloudSession = '000000'
dCloudDC = 'N/A'
dCloudPOD = 'POD %s (%s)' % (dCloudSession, dCloudDC)  


# APIC-EM info
def form_apic_em_status_spark_message():
    headers = {'Content-type': 'application/json'}
    data = {'username': _LabEnv.APIC_EM_USR,
            'password': _LabEnv.APIC_EM_PWD}
    try:
        response = requests.post(_LabEnv.APIC_EM_API + APIC_EM_AUTH_ENDPOINT, json=data,
                                 headers=headers, verify=False)
        response.raise_for_status()
        spark_message = u'{} APIC-EM Login {}\n'.format(CHECK_MARK_SYMBOL, response.json()['response'])
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        spark_message = u'{} Connection to APIC-EM server {} was unsuccessful\n'.format(
            CROSS_MARK_SYMBOL, _LabEnv.APIC_EM_HOST
        )
    return spark_message


lab_state += form_apic_em_status_spark_message()

# ############################################################################
# Post into Spark Room
# ############################################################################
# messagetext = 'Hello %s this is %s on %s\n%s' % (_LabEnv.LAB_SESSION, _LabEnv.LAB_USER, dCloudPOD, labstate)
spark_message = u'Hello {}! This is {} \n{}'.format(_LabEnv.LAB_SESSION, _LabEnv.LAB_USER, lab_state)
r = _LabEnv.postSparkMessage(spark_message)

# ############################################################################
# EOF
# ############################################################################