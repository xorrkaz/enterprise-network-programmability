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

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests  # noqa

import env  # noqa
import constants  # noqa

SPARK_API_ROOT = 'https://api.ciscospark.com/v1'
SPARK_API_MESSAGES_ENDPOINT = '/messages'
SPARK_API_ROOMS_ENDPOINT = '/rooms'
SPARK_ROOM_ID_FILENAME = 'SPARK_ROOM_ID.txt'

RESTCONF_CHECK_ENDPOINT = 'https://{}/.well-known/host-meta'.format(constants.CSR_HOST)


class SparkRoomNotFound(Exception):
    pass


class SparkAPIKeyNotFound(Exception):
    pass


class RESTCONFNotRunning(Exception):
    pass


def get_spark_api_token():
    """Looks for and returns the SPARK API token in environmental variables and env.py file.

    Returns:
        str: SPARK API token

    Raises:
        SparkAPIKeyNotFound exception - when spark API token was not found
    """
    api_token = os.environ.get('SPARK_API_TOKEN')
    if api_token is None:
        env_spark_user_token = env.LAB_USER_SPARK_TOKEN
        if env_spark_user_token == 'YOUR-ACCESS-TOKEN-HERE':
            raise SparkAPIKeyNotFound('Spark API key was not specified as an environmental variable or in env.py')
        else:
            api_token = env_spark_user_token
    return api_token


def get_spark_room_id(room_name=None, write_to_file=True):
    """Looks for and returns the Spark Room ID

    The following places are searched:
        1) environmental variable 'SPARK_ROOM_ID'
        2) file SPARK_ROOM_ID.txt in tasks/ directory
        3) using SPARK api based on room_name. If room_name is specified, use only step 3).
        Otherwise, use room_name specified in env.py under variable SPARK_ROOM_NAME


    Args:
        room_name (str): name of the room for which id is being searched
        write_to_file (boolean): shows if room_id should be written to the file SPARK_ROOM_ID.txt in tasks/ directory

    Returns:
        str: room_id

    Raises:
        SparkRoomNotFound exception - when the room with the given title was not found
    """
    def get_room_id_via_api(room_name):
        api_token = get_spark_api_token()
        headers = {'Authorization': 'Bearer {}'.format(api_token),
                   'Content-Type': 'application/json'}

        response = requests.get(SPARK_API_ROOT + SPARK_API_ROOMS_ENDPOINT, headers=headers)
        response.raise_for_status()

        for room in response.json()['items']:
            if room['title'] == room_name:
                room_id = room['id']
                return room_id

        raise SparkRoomNotFound('Spark room with the title "{}" was not found. Check if the name is correct'.format(
            room_name
        ))

    spark_room_id_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), SPARK_ROOM_ID_FILENAME)
    if room_name is None:
        room_id = os.environ.get('SPARK_ROOM_ID')
        if room_id is None:
            if os.path.isfile(spark_room_id_file_path):
                with open(spark_room_id_file_path) as f:
                    room_id = f.read()
                    write_to_file = False
            else:
                room_id = get_room_id_via_api(env.SPARK_ROOM_NAME)
    else:
        room_id = get_room_id_via_api(room_name)

    if write_to_file:
        with open(spark_room_id_file_path, 'w') as f:
            f.write(room_id)

    return room_id


def send_spark_message(markdown=None, message=None, room_id=None, api_token=None):
    """Sends a message to spark room

    Either markdown or plain text message may be sent. Room_id and api_token are being searched in several places.

    Args:
        markdown (str): markdown message to be sent to the spark room
        message (str): plain text message to be sent to the spark room
        room_id (str): spark room id where to post messages
        api_token (str): token to use spark API

    Returns:
        None
    """
    if api_token is None:
        api_token = get_spark_api_token()

    if room_id is None:
        room_id = get_spark_room_id()

    headers = {'Authorization': 'Bearer {}'.format(api_token),
               'Content-Type': 'application/json'}

    if message is not None:
        data = {'text': message,
                'roomId': room_id}
    else:
        data = {'markdown': markdown,
                'roomId': room_id}

    response = requests.post(SPARK_API_ROOT + SPARK_API_MESSAGES_ENDPOINT,
                             headers=headers, json=data)

    response.raise_for_status()
    print('Spark message has been successfully sent.')


def check_restconf():
    """Checks if RESTCONF is operational by querying /.well-known/host-meta per RFC.

    Returns:
        None

    Raises:
        RESTCONFNotRunning exception if RESTCONF service is not operational
    """
    try:
        response = requests.get(RESTCONF_CHECK_ENDPOINT, verify=False,
                                auth=(constants.CSR_USERNAME, constants.CSR_PASSWORD))
        response.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        raise RESTCONFNotRunning('Operation is unsuccessful. '
                                 'Verify that RESTCONF and HTTPS server are enabled.')