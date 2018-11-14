'''
This script prepares data in the format for the testing
algorithms to run

Author: Anton Yeshchenko
'''

import csv

from formula_verificator import generateXLog


def generateXesLog(eventlog):
    csvfile = open('../data/%s' % eventlog, 'r')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)  # skip the headers

    trace_activity = []
    trace_group = []
    trace_time = []

    traces_id = []
    traces_activity = []
    traces_group = []
    traces_time = []

    last_case = ''
    first_line = True

    for row in spamreader:
        if row[0] != last_case:
            last_case = row[0]
            if not first_line:
                traces_activity.append(trace_activity)
                traces_group.append(trace_group)
                traces_time.append(trace_time)
            traces_id.append(last_case)
            trace_activity = []
            trace_group = []
            trace_time = []
        trace_activity.append(row[1])
        trace_group.append(row[3])
        trace_time.append(row[2])
        first_line = False

    traces_activity.append(trace_activity)
    traces_group.append(trace_group)
    traces_time.append(trace_time)

    generateXLog(traces_id, traces_activity, traces_group, traces_time)
