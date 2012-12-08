from __future__ import with_statement

import re
import os
import tempfile

from PySide import QtCore

def launch_tor(tor_cmd="tor", args=[], torrc_path=None):
    """
    Launches a tor process.

    :param str tor_cmd: tor command to execute
    :param list args: list of args to pass to the tor process
    :param str torrc_path: path to torrc file

    :returns: **QtCore.QProcess** QProcess instance
    """

    config = {
        'ControlPort': 9051,
        'ControlListenAddress' : '127.0.0.1:9051'
    }

    if not torrc_path:
        torrc_path = make_torrc(config)

    args += ['-f', torrc_path]
    tor_process = QtCore.QProcess()
    tor_process.start(tor_cmd, args)

    return tor_process, torrc_path

def make_torrc(config):
    """
    Creates a temporary torrc file.

    :param dic config" config options for torrc

    :returns: **str** path to the new torrc
    """

    torrc_path = tempfile.mkstemp(prefix = "torrc-", text = True)[1]


    with open(torrc_path, "w") as torrc_file:
        for key, value in config.items():
            torrc_file.write("%s %s\n" % (key, value))

    return torrc_path

def parse_bootstrap_msg(msg):
    """
    Returns how much % of bootstrapping has been completed.

    :param str msg: input message to be parsed

    :returns: **int** numerical value of % bootstrapping done
    """

    bootstrap_line = re.compile("Bootstrapped ([0-9]+)%: ")
    bootstrap_match = bootstrap_line.search(msg)
    if bootstrap_match:
        return int(bootstrap_match.groups()[0])

def parse_torrc(torrc):
    """
    Returns a dict with all the key value mappings in a torrc

    :param str msg: path to torrc file

    :returns: **dict** key value mappings of torrc
    """

    torrc_val = {}

    with open(torrc) as torrc_fh:
        for line in torrc_fh.readlines():
            line = line.strip()
            if line.startswith('#'):
                continue
            else:
                key, val = line.split(' ')
                torrc_val[key] = val

    return torrc_val
