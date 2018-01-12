#!/usr/bin/env python
# ############################################################################
# Copyright (c) 2018 Joe Clarke and Dmitry Figol, Cisco Systems
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
import re

import dna

BACKUP_CONFIG_IOS_PATH = 'flash:/running-config.bak'


def parse_arguments():
    """

    Returns:

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--spark-room-id', help='Spark ROOM ID')
    parser.add_argument('-f', '--backup-config-ios-path', default=BACKUP_CONFIG_IOS_PATH,
                        help='Path on IOS where running configuration should be saved')
    # Hidden parameters
    parser.add_argument('-d', '--test-dir', help=argparse.SUPPRESS)
    args = parser.parse_args()
    return args


def convert_ios_path_to_linux(path):
    path_components = os.path.normpath(path).split(os.sep)
    file_system = path_components[0]

    if ':' in file_system:
        file_system = file_system.strip(':')
        path_components = path_components[1:]
    else:
        file_system = 'flash'

    result_path = os.path.join(os.sep, file_system, *path_components)
    return result_path


def save_config_to_ios_file(backup_config_ios_path=BACKUP_CONFIG_IOS_PATH, override=True):
    dna.configure('file prompt quiet')

    backup_config_linux_path = convert_ios_path_to_linux(backup_config_ios_path)

    if override:
        dna.run_exec_command('copy running-config {}'.format(backup_config_ios_path))
    else:
        if not os.path.isfile(backup_config_linux_path):
            dna.run_exec_command('copy running-config {}'.format(backup_config_ios_path))

    print('Running configuration was saved to {}'.format(backup_config_ios_path))


def get_config_diff(backup_config_ios_path):
    """

    Args:
        backup_config_ios_path:

    Returns:

    """
    config_diff = dna.get_output(
        'show archive config diff {} system:running-config'.format(backup_config_ios_path)
    )
    backup_config_linux_path = convert_ios_path_to_linux(backup_config_ios_path)
    os.remove(backup_config_linux_path)
    dna.run_exec_command('copy running-config {}'.format(backup_config_ios_path))

    if re.search('No changes were found', config_diff):
        return None
    else:
        config_diff_lines = re.split(r'\r?\n', config_diff)
        return config_diff_lines


def form_spark_message(config_diff_lines):
    """

    Args:
        config_diff_lines:

    Returns:

    """
    message = 'Configuration differences between the running config and the last backup:\n```\n{}\n```'.format(
        '\n'.join(config_diff_lines)
    )
    return message


def main():
    """

    Returns:

    """
    args = parse_arguments()
    backup_config_linux_path = convert_ios_path_to_linux(args.backup_config_ios_path)

    if not os.path.isfile(backup_config_linux_path):
        save_config_to_ios_file(args.backup_config_ios_path)
        print('Running-config file is saved for the first time, exiting.')

    else:
        config_diff_lines = get_config_diff(args.backup_config_ios_path)
        if config_diff_lines is not None:
            print('Changes have been found.')
            message = form_spark_message(config_diff_lines)
            dna.send_spark_message(markdown=message)
        else:
            print('No configuration changes have been found.')


if __name__ == '__main__':
    main()
