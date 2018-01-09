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
import os
from pkgutil import find_loader


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
        filename = '{}.txt'.format(cli_command)
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
