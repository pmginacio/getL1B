#!/usr/bin/env python
# -*- coding: utf-8; -*-
'''A random selection of general purpose functions'''

__author__ = "Pedro Inácio"
__copyright__ = "Copyright 2015"
__version__ = "1.0"
__maintainer__ = "Pedro Inácio"
__email__ = "pedro@inacio.space"
__status__ = "Development"

import calendar
from datetime import date, timedelta
import subprocess


def parse_date_range(dstr):
    """This function parses a date range with the format:
        YYYY[MM[DD]][:YYYY[MM[DD]]]
    and returns a tuple with the initial and final dates.

    Possible '-'' and '/'' characters on the input string are stripped.
    """

    # Remove - and / and split into lower and upper date bounds
    date_range = dstr.replace('-', '').replace('/', '').split(':')

    # Check length
    if len(date_range) == 0 or len(date_range) >= 3:
        raise ValueError("Incorrectly specified date range")

    # Parse lower bound of data range
    date_start = parse_date(date_range[0])

    # Parse optional upper bound of date range
    if len(date_range) == 1:
        date_end = parse_date(date_range[0], round_up=True)
    else:
        date_end = parse_date(date_range[1], round_up=True)

    # Check valid range
    if date_start > date_end:
        raise ValueError("Incorrect date range. Upper bound of date range " +
                         "must be later than lower bound.")

    # Return tuple
    return (date_start, date_end)


def parse_date(dstr, round_up=False):
    """This function recieves a string with the format YYYY[MM[DD]] and returns
    the corresponding date object.
    Missing elements are assumed to be 1, i.e., 2006 corresponds to 2006/01/01

    Optional argument round_up specifies whether to round the date up instead,
    i.e., 2006 corresponds to 2006/12/31
    """

    year = int(dstr[0:4])
    if round_up:
        month = int(dstr[4:6]) if dstr[4:6] != '' else 12
        # get last day of the month
        aux = calendar.monthrange(year, month)
        day = int(dstr[6:8]) if dstr[6:8] != '' else aux[1]
    else:
        month = int(dstr[4:6]) if dstr[4:6] != '' else 1
        day = int(dstr[6:8]) if dstr[6:8] != '' else 1

    return date(year, month, day)


def range_date(date_start, date_end, delta=timedelta(1)):
    """Similar to the range function, return a list of dates"""

    list_dates = list()
    d = date_start
    while d <= date_end:
        list_dates.append(d)
        d += delta

    return list_dates


def call(cmd, live=False):
    """Execute a command in the shell and returns stdout as string.

    Optional argument live directly prints stdout trought pythons terminal

    If the command fails, an exception is raised with stderr
    """

    if live:
        # call command
        return_code = subprocess.call(cmd, shell=True)

        # output already printed to the terminal
        output = ["", ""]
    else:
        # create call object
        callObj = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)

        # wait for execution to finish and get (stdout,stderr) tuple
        output = callObj.communicate()

        # collect return code
        return_code = callObj.returncode

    # check return code
    if return_code != 0:
        # return stderr
        raise RuntimeError(output[1])
    else:
        # return stdout
        return output[0]


def check_utilities_in_system(list_utils):
    """Check if the requested list of programs is available in the system."""

    # Handle non-list elements
    if not isinstance(list_utils, list):
        list_utils = [list_utils]

    # Loop and check it exists
    for x in list_utils:
        try:
            call("type "+x)
        except RuntimeError, e:
            raise Exception("Could not find '"+x+"' available in this system")


def confirm(prompt=None, resp=False):
    """Prompts for 'yes' or 'no' response from the user. Returns True for 'yes'
    and False for 'no'.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True
    """
    # Created by Raghuram Devarakonda
    # Obtained from:
    # http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False
