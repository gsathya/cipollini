import re

from PySide import QtCore

def launch_tor():
    tor_cmd = "tor"
    args = []
    
    tor_process = QtCore.QProcess()
    tor_process.start(tor_cmd, args)

    return tor_process

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
