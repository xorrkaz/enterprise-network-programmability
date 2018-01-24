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

import sqlite3
import sys
from time import gmtime, strftime

# Log CLI commands to a local SQLite3 database

DB_FILE_PATH = '/flash/aaa.db'

# Schema is: Timestamp, Username, Host, Privilege, Command, Result_Code
CREATE_SQL = 'CREATE TABLE IF NOT EXISTS command_history (ts, username, host, privilege, command, result_code)'
INSERT_SQL = 'INSERT INTO command_history VALUES (:time, :user, :host, :priv, :command, :rc)'


def get_command_details():
    result = {'time': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
              'user': sys.argv[1], 'host': sys.argv[2],
              'priv': sys.argv[3], 'command': sys.argv[4],
              'rc': sys.argv[5]}
    return result


def get_db_connector():
    connection = sqlite3.connect(DB_FILE_PATH)
    cursor = connection.cursor()
    cursor.execute(CREATE_SQL)
    return connection


def record_command(connection):
    cursor = connection.cursor()
    cursor.execute(INSERT_SQL, get_command_details())
    connection.commit()


def main():
    connection = get_db_connector()
    record_command(connection)
    connection.close()


if __name__ == '__main__':
    main()
