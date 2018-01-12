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

import argparse
import ftplib
import os
from pkgutil import find_loader

import requests

SPARK_API_ROOT = 'https://api.ciscospark.com/v1'
SPARK_API_MESSAGES_ENDPOINT = '/messages'


class SparkRoomNotFound(Exception):
    pass


class SparkAPIKeyNotFound(Exception):
    pass


def is_debug_environment():
    """Checks if cli library exists

    Returns:
        boolean, False, if cli library exists, True - otherwise

    """
    return find_loader('cli') is None


def get_test_dir_argument():
    """

    Returns:

    """
    try:
        return get_test_dir_argument.test_dir
    except AttributeError:
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--test-dir', help=argparse.SUPPRESS)
        args, unknown = parser.parse_known_args()
        test_dir = args.test_dir
        if test_dir is None:
            raise parser.error('Running in debug environment, but argument --test-dir was not provided')
        get_test_dir_argument.test_dir = test_dir
        return test_dir


def get_output(command):
    """Shows output from running the command or opening a file if cli library is not present

    Args:
        command: string, command to be run if tac.DEBUG is set or
            path of the file to open, otherwise

    Returns:
        string - command execution output
    """
    if is_debug_environment():
        dir_name = get_test_dir_argument()
        filename = '{}.txt'.format(command)
        full_path = os.path.join(dir_name, filename)
        if os.path.isfile(full_path):
            with open(full_path) as f:
                return f.read()
        raise IOError("File {} is not found".format(full_path))
    else:
        import cli
        result = cli.cli(command)
        i = 0
        # Occasionally, cli library returns an empty output, in this case we try multiple time
        while result.count('\n') <= 2 and i < 3:
            result = cli.cli(command)
            i += 1
        return result


def run_exec_command(command):
    """Returns output from running a command in EXEC mode.

    Use for debug/configuration commands in EXEC mode (like EPC, packet tracer, etc.)
    For show commands use get_output
    You may have multiple commands separated by ;

    Examples:
        >>> run_exec_command("debug crypto ipsec")
        >>> run_exec_command("debug platform condition int g1 both ; debug plat cond start all")

    Args:
        command: string, command to be run

    Returns:
        string, command execution output
    """
    if not is_debug_environment():
        import cli
        return cli.cli(command)


def configure(configuration):
    """Apply configuration to the device.

    Configure terminal is entered automatically.

    Examples:
        >>> configuration = '''interface lo0
             shutdown'''
        >>> configure(configuration)

    Args:
        configuration: string, configuration commands separated by \n

    Returns:
        string, output (if any) from applying configuration
    """
    if not is_debug_environment():
        import cli
        return cli.configure(configuration)


def upload_file_to_ftp(src_file_path, dst_file_path, host, username='anonymous', password='anonymous'):
    """Uploads a file to FTP server

    Args:
        src_file_path: string, the path to the source file
        dst_file_path: string, the path to the destination file on FTP server
        host: string, FTP server IP or DNS name
        username: string, username. Default is 'anonymous'
        password: string, password. Default is 'anonymous'

    Returns:
        None
    """
    ftp = ftplib.FTP(host, timeout=30)
    ftp.login(username, password)
    dst_file_name = os.path.basename(dst_file_path)
    for directory in os.path.normpath(dst_file_path).split(os.sep)[:-1]:
        if directory:
            if directory not in ftp.nlst():
                ftp.mkd(directory)
            ftp.cwd(directory)

    with open(src_file_path, 'rb') as f:
        ftp.storbinary("STOR {}".format(dst_file_name), f)
    print('Successfully uploaded file {} to FTP {}'.format(dst_file_path, host))


def send_spark_message(message=None, markdown=None, room_id=None, api_token=None):
    """

    Args:
        message:
        markdown:
        room_id:
        api_token:

    Returns:

    """
    if room_id is None:
        room_id = os.environ.get('SPARK_ROOM_ID')
        if room_id is None:
            raise SparkRoomNotFound('Spark Room ID was not specified as a command line'
                                    'argument or environmental variable')

    if api_token is None:
        api_token = os.environ.get('SPARK_API_TOKEN')
        if api_token is None:
            raise SparkAPIKeyNotFound('Spark API key was not specified as an environmental variable')

    headers = {'Authorization': 'Bearer {}'.format(api_token),
               'Content-Type': 'application/json'}

    if message is not None:
        data = {'text': message,
                'roomId': room_id}
    else:
        data = {'markdown': markdown,
                'roomId': room_id}

    r = requests.post(SPARK_API_ROOT + SPARK_API_MESSAGES_ENDPOINT,
                      headers=headers, json=data)

    if r.status_code == 200:
        print('Spark message has been posted.')
    else:
        r.raise_for_status()

