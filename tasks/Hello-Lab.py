#!/usr/bin/env python
# ############################################################################
# Copyright (c) 2018 Bruno Klauser <bklauser@cisco.com>
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
import json
import requests
import sys
# Disable Certificate warning
try:
  requests.packages.urllib3.disable_warnings()
except:
  pass

# ############################################################################
# Variables below
# ############################################################################
SPARK_ROOM_ID = None

# ############################################################################
# Find (or Create) Spark Room
# ############################################################################
r = requests.get(_LabEnv.SPARK_API_ROOMS, headers=_LabEnv.SPARK_HEADERS, verify=False)
j = json.loads(r.text)

for tmproom in j['items']:
  if tmproom['title'] == _LabEnv.SPARK_ROOM_NAME:
    SPARK_ROOM_ID = tmproom['id']
    print("Found room ID for '" + _LabEnv.SPARK_ROOM_NAME + "' : " + SPARK_ROOM_ID)
    break
    
if SPARK_ROOM_ID is None:
  print("Failed to find room ID for '" + _LabEnv.SPARK_ROOM_NAME + " creating it ...'")
  t = json.dumps({'title':_LabEnv.SPARK_ROOM_NAME})
  # print('Spark Request: ' + t)
  r = requests.post(_LabEnv.SPARK_API_ROOMS, data=t, headers=_LabEnv.SPARK_HEADERS, verify=False)
  # print('Spark Response: ' + r.text)
  j = json.loads(r.text)  
  SPARK_ROOM_ID = j['id']

if SPARK_ROOM_ID is None:
  print("Failed to find or create room ID for '" + _LabEnv.SPARK_ROOM_NAME + "'")
  sys.exit(1)

# ############################################################################
# Verify Lab Environment
# ############################################################################

ucgood = '\u2705' 
ucbad =  '\u274C'

# Python Version and Platform info
labstate = ucgood + ' Python ('+sys.version+' on '+sys.platform+')\n'

# Spark Room info
labstate = labstate + ucgood + ' Spark Room (ID='+SPARK_ROOM_ID+')\n'

# dCloud Session info
# TBD once session.xml is provisioned
dCloudSession = '000000'
dCloudDC = 'N/A'
dCloudPOD = 'POD %s (%s)' % (dCloudSession, dCloudDC)  

# APIC-EM info
apic_credentials = json.dumps({'username':_LabEnv.APIC_EM_USR,'password':_LabEnv.APIC_EM_PWD})
tmp_headers = {'Content-type': 'application/json'}
tmp_post = '%s/ticket' % _LabEnv.APIC_EM_API
r = requests.post(tmp_post, data=apic_credentials, verify=False, headers=tmp_headers)
labstate = labstate + ucgood + ' APIC-EM Login '+ str(r.json()['response']) +')\n'

# ############################################################################
# Post into Spark Room
# ############################################################################
# messagetext = 'Hello %s this is %s on %s\n%s' % (_LabEnv.LAB_SESSION, _LabEnv.LAB_USER, dCloudPOD, labstate)
messagetext = 'Hello %s this is %s \n%s' % (_LabEnv.LAB_SESSION, _LabEnv.LAB_USER, labstate)
r = _LabEnv.postSparkMessage(messagetext)

# ############################################################################
# EOF
# ############################################################################