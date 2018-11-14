"""
this script trains an LSTM model on one of the data files in the data folder of
this repository. the input file can be changed to another file from the data folder
by changing its name in line 46.

it is recommended to run this script on GPU, as recurrent networks are quite
computationally intensive.

Author: Niek Tax
"""

from __future__ import print_function, division

import copy
import csv
import time
from datetime import datetime
from itertools import izip
import os

import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.layers import Input, Dropout
from keras.layers.core import Dense
from keras.layers.recurrent import LSTM
from keras.models import Model

from shared_variables import get_unicode_from_int, activate_settings


def build_model(max_len, num_features, target_chars):
    print('Build model...')
    main_input = Input(shape=(max_len, num_features), name='main_input')
    processed = main_input

    processed = LSTM(128, return_sequences=False)(processed)
    processed = Dropout(0.5)(processed)
    processed = Dense(64, activation='relu')(processed)
    processed = Dropout(0.5)(processed)
    act_output = Dense(len(target_chars), activation='softmax', name='act_output')(processed)
    time_output = Dense(1, activation='relu', name='time_output')(processed)

    model = Model(main_input, [act_output, time_output])

    model.compile(loss={'act_output': 'categorical_crossentropy', 'time_output': 'mae'}, optimizer='adam')
    return model


def create_checkpoints_path(log_name):
    folder_path = 'output_files/final_experiments/models/CF/' + log_name
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    checkpoint_name = folder_path + '/model_{epoch:03d}-{val_loss:.3f}.h5'
    return checkpoint_name


def train_model(model, checkpoint_name, X, y_a, y_t):
    model_checkpoint = ModelCheckpoint(checkpoint_name, save_best_only=True)
    lr_reducer = ReduceLROnPlateau(factor=0.5, patience=10, verbose=0)
    early_stopping = EarlyStopping(monitor='val_loss', patience=30)

    model.fit(X, {'act_output': y_a, 'time_output': y_t},
              validation_split=0.2,
              verbose=2,
              callbacks=[early_stopping, model_checkpoint, lr_reducer],
              epochs=300)


def train(log_identificator):
    eventlog = activate_settings(log_identificator)[0]
    lines = []  # list of all the activity sequences
    timeseqs = []  # time sequences (differences between two events)
    timeseqs2 = []  # time sequences (differences between the current and first)

    # helper variables
    lastcase = ''
    line = ''  # sequence of activities for one case
    firstline = True
    times = []
    times2 = []
    numlines = 0
    casestarttime = None
    lasteventtime = None

    csvfile = open('../data/final_experiments/%s.csv' % eventlog, 'r')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)  # skip the headers

    for row in spamreader:  # the rows are "CaseID,ActivityID,CompleteTimestamp"
        t = time.strptime(row[2], "%Y-%m-%d %H:%M:%S")  # creates a datetime object from row[2]
        if row[0] != lastcase:  # 'lastcase' is to save the last executed case for the loop
            casestarttime = t
            lasteventtime = t
            lastcase = row[0]
            if not firstline:  # here we actually add thesequences to the lists
                lines.append(line)
                timeseqs.append(times)
                timeseqs2.append(times2)
            line = ''
            times = []
            times2 = []
            numlines += 1
        line += get_unicode_from_int(row[1])
        timesincelastevent = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(time.mktime(lasteventtime))
        timesincecasestart = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(time.mktime(casestarttime))
        timediff = 86400 * timesincelastevent.days + timesincelastevent.seconds
        timediff2 = 86400 * timesincecasestart.days + timesincecasestart.seconds
        times.append(timediff)
        times2.append(timediff2)
        lasteventtime = t
        firstline = False

    # add last case
    lines.append(line)
    timeseqs.append(times)
    timeseqs2.append(times2)
    numlines += 1

    divisor = np.mean([item for sublist in timeseqs for item in sublist])  # average time between events
    print('divisor: {}'.format(divisor))
    divisor2 = np.mean([item for sublist in timeseqs2 for item in sublist])  # average time between current and
    # first events
    print('divisor2: {}'.format(divisor2))

    # separate training data into 2(out of 3) parts
    elems_per_fold = int(round(numlines / 3))

    many = 0
    for i in range(len(lines)):
        many = many + len(lines[i])

    print("average length of the trace: ", many / len(lines))
    print("number of traces: ", len(lines))

    fold1 = lines[:elems_per_fold]
    fold2 = lines[elems_per_fold:2 * elems_per_fold]
    lines = fold1 + fold2

    lines = map(lambda x: x + '!', lines)  # put delimiter symbol
    maxlen = max(map(lambda x: len(x), lines))  # find maximum line size

    # next lines here to get all possible characters for events and annotate them with numbers
    chars = map(lambda x: set(x), lines)  # remove duplicate activities from each separate case
    chars = list(set().union(*chars))  # creates a list of all the unique activities in the data set
    chars.sort()  # sorts the chars in alphabetical order
    target_chars = copy.copy(chars)
    chars.remove('!')
    print('total chars: {}, target chars: {}'.format(len(chars), len(target_chars)))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    target_char_indices = dict((c, i) for i, c in enumerate(target_chars))

    csvfile = open('../data/final_experiments/%s.csv' % eventlog, 'r')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)  # skip the headers
    lastcase = ''
    line = ''
    firstline = True
    lines = []
    timeseqs = []
    timeseqs2 = []
    timeseqs3 = []
    timeseqs4 = []
    times = []
    times2 = []
    times3 = []
    times4 = []
    numlines = 0
    casestarttime = None
    lasteventtime = None
    for row in spamreader:
        t = time.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        # new case starts
        if row[0] != lastcase:
            casestarttime = t
            lasteventtime = t
            lastcase = row[0]
            if not firstline:
                lines.append(line)
                timeseqs.append(times)
                timeseqs2.append(times2)
                timeseqs3.append(times3)
                timeseqs4.append(times4)
            line = ''
            times = []
            times2 = []
            times3 = []
            times4 = []
            numlines += 1
        line += get_unicode_from_int(row[1])
        timesincelastevent = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(time.mktime(lasteventtime))
        timesincecasestart = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(time.mktime(casestarttime))
        midnight = datetime.fromtimestamp(time.mktime(t)).replace(hour=0, minute=0, second=0, microsecond=0)
        timesincemidnight = datetime.fromtimestamp(time.mktime(t)) - midnight
        timediff = 86400 * timesincelastevent.days + timesincelastevent.seconds
        timediff2 = 86400 * timesincecasestart.days + timesincecasestart.seconds
        timediff3 = timesincemidnight.seconds  # this leaves only time even occured after midnight
        timediff4 = datetime.fromtimestamp(time.mktime(t)).weekday()  # day of the week
        times.append(timediff)
        times2.append(timediff2)
        times3.append(timediff3)
        times4.append(timediff4)
        lasteventtime = t
        firstline = False

    # add last case
    lines.append(line)
    timeseqs.append(times)
    timeseqs2.append(times2)
    timeseqs3.append(times3)
    timeseqs4.append(times4)
    numlines += 1

    elems_per_fold = int(round(numlines / 3))
    fold1 = lines[:elems_per_fold]
    fold1_t = timeseqs[:elems_per_fold]
    fold1_t2 = timeseqs2[:elems_per_fold]
    fold1_t3 = timeseqs3[:elems_per_fold]
    fold1_t4 = timeseqs4[:elems_per_fold]

    with open('output_files/folds/fold1.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row, timeseq in izip(fold1, fold1_t):
            spamwriter.writerow([unicode(s).encode("utf-8") + '#{}'.format(t) for s, t in izip(row, timeseq)])

    fold2 = lines[elems_per_fold:2 * elems_per_fold]
    fold2_t = timeseqs[elems_per_fold:2 * elems_per_fold]
    fold2_t2 = timeseqs2[elems_per_fold:2 * elems_per_fold]
    fold2_t3 = timeseqs3[elems_per_fold:2 * elems_per_fold]
    fold2_t4 = timeseqs4[elems_per_fold:2 * elems_per_fold]
    with open('output_files/folds/fold2.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row, timeseq in izip(fold2, fold2_t):
            spamwriter.writerow([unicode(s).encode("utf-8") + '#{}'.format(t) for s, t in izip(row, timeseq)])

    fold3 = lines[2 * elems_per_fold:]
    fold3_t = timeseqs[2 * elems_per_fold:]
    with open('output_files/folds/fold3.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row, timeseq in izip(fold3, fold3_t):
            spamwriter.writerow([unicode(s).encode("utf-8") + '#{}'.format(t) for s, t in izip(row, timeseq)])

    lines = fold1 + fold2
    lines_t = fold1_t + fold2_t
    lines_t2 = fold1_t2 + fold2_t2
    lines_t3 = fold1_t3 + fold2_t3
    lines_t4 = fold1_t4 + fold2_t4

    step = 1
    sentences = []
    softness = 0
    next_chars = []
    lines = map(lambda x: x + '!', lines)

    sentences_t = []
    sentences_t2 = []
    sentences_t3 = []
    sentences_t4 = []
    next_chars_t = []
    next_chars_t2 = []
    next_chars_t3 = []
    next_chars_t4 = []
    for line, line_t, line_t2, line_t3, line_t4 in izip(lines, lines_t, lines_t2, lines_t3, lines_t4):
        for i in range(0, len(line), step):
            if i == 0:
                continue

            # we add iteratively, first symbol of the line, then two first, three...
            sentences.append(line[0: i])
            sentences_t.append(line_t[0:i])
            sentences_t2.append(line_t2[0:i])
            sentences_t3.append(line_t3[0:i])
            sentences_t4.append(line_t4[0:i])
            next_chars.append(line[i])
            if i == len(line) - 1:  # special case to deal time of end character
                next_chars_t.append(0)
                next_chars_t2.append(0)
                next_chars_t3.append(0)
                next_chars_t4.append(0)
            else:
                next_chars_t.append(line_t[i])
                next_chars_t2.append(line_t2[i])
                next_chars_t3.append(line_t3[i])
                next_chars_t4.append(line_t4[i])
    print('nb sequences:', len(sentences))

    print('Vectorization...')
    num_features = len(chars) + 5
    print('num features: {}'.format(num_features))
    X = np.zeros((len(sentences), maxlen, num_features), dtype=np.float32)
    y_a = np.zeros((len(sentences), len(target_chars)), dtype=np.float32)
    y_t = np.zeros((len(sentences)), dtype=np.float32)
    for i, sentence in enumerate(sentences):
        leftpad = maxlen - len(sentence)
        next_t = next_chars_t[i]
        sentence_t = sentences_t[i]
        sentence_t2 = sentences_t2[i]
        sentence_t3 = sentences_t3[i]
        sentence_t4 = sentences_t4[i]
        for t, char in enumerate(sentence):
            # multiset_abstraction = Counter(sentence[:t+1])
            for c in chars:
                if c == char:  # this will encode present events to the right places
                    X[i, t + leftpad, char_indices[c]] = 1
            X[i, t + leftpad, len(chars)] = t + 1
            X[i, t + leftpad, len(chars) + 1] = sentence_t[t] / divisor
            X[i, t + leftpad, len(chars) + 2] = sentence_t2[t] / divisor2
            X[i, t + leftpad, len(chars) + 3] = sentence_t3[t] / 86400
            X[i, t + leftpad, len(chars) + 4] = sentence_t4[t] / 7
        for c in target_chars:
            if c == next_chars[i]:
                y_a[i, target_char_indices[c]] = 1 - softness
            else:
                y_a[i, target_char_indices[c]] = softness / (len(target_chars) - 1)
        y_t[i] = next_t / divisor

    model = build_model(maxlen, num_features, target_chars)
    checkpoint_name = create_checkpoints_path(eventlog)
    train_model(model, checkpoint_name, X, y_a, y_t)
