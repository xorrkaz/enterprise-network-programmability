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
import os
from datetime import datetime

import dna


def parse_arguments():
    """

    Returns:

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--commands', required=True,
                        help='The list of commands separated by "; ". '
                              'The list should be limited by double quotes')
    parser.add_argument('-H', '--host', help='IP or domain name of FTP server')
    parser.add_argument('-u', '--username', help='username for FTP server')
    parser.add_argument('-p', '--password', help='password for FTP server')
    parser.add_argument('-s', '--spark-room-id', help='Spark ROOM ID')
    # Hidden parameters
    parser.add_argument('-d', '--test-dir', help=argparse.SUPPRESS)
    args = parser.parse_args()
    return args


def collect_outputs(commands):
    result = []
    for command in commands.split(';'):
        command = command.strip()
        result.append('\n\n----- command executed from guestshell: #{} -----\n\n{}'.format(
            command, dna.get_output(command)
        ))
    return ''.join(result)


def write_outputs_to_file(result):
    if dna.is_debug_environment():
        dir_name = os.path.dirname(os.path.dirname(os.getcwd()))
        dir_name = os.path.join(dir_name, 'tests/files/tmp')
    else:
        dir_name = '/bootflash'

    filename = '{}_outputs.txt'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))
    full_path = os.path.join(dir_name, filename)

    with open(full_path, 'w') as f:
        f.write(result)

    print('Successfully written file {}'.format(full_path))
    return full_path


def main():
    args = parse_arguments()
    result = collect_outputs(args.commands)
    full_path = write_outputs_to_file(result)
    dst_file_path = os.path.join('outputs', os.path.basename(full_path))
    dna.upload_file_to_ftp(src_file_path=full_path, dst_file_path=dst_file_path,
                           host=args.host, username=args.username, password=args.password)
    dna.send_spark_message(markdown='The file containing outputs `{}` has been uploaded to FTP {}'
                                    ' and is available here: `{}`'.format(args.commands, args.host, dst_file_path))


if __name__ == '__main__':
    main()
