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
# Always check for the latest Version of this script via http://cs.co/NWPLab
# ############################################################################

import argparse

import dna


def parse_arguments():
    """

    Returns:

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--commands', help='The list of commands separated by "; ". '
                                                 'The list should be limited by double quotes')
    parser.add_argument('-H', '--hostname', help='Hostname of FTP server')
    parser.add_argument('-u', '--username', help='username for FTP server')
    parser.add_argument('-p', '--password', help='password for FTP server')
    parser.add_argument('-s', '--spark-room-id', help='ID of the Spark room where notifications are posted')
    # Hidden parameters
    parser.add_argument('-d', '--test-dir', help=argparse.SUPPRESS)
    args = parser.parse_args()
    return args


def collect_outputs():
    args = parse_arguments()


def main():
    collect_outputs()


if __name__ == '__main__':
    main()