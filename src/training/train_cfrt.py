"""
This script takes as input the workflow, timestamps and an event attribute "resource"
It makes predictions on the workflow & timestamps and the event attribute "resource"

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

import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Input, Dropout, BatchNormalization, LeakyReLU
from keras.layers.core import Dense
from keras.layers.recurrent import LSTM
from keras.models import Model

import shared_variables
from shared_variables import get_unicode_from_int, epochs, validation_split, folds
from training.train_common import create_checkpoints_path


class TrainCFRT:
    def __init__(self):
        pass

    @staticmethod
    def _build_model(max_len, num_features, target_chars, target_chars_time, target_chars_group, use_old_model):
        print('Build model...')
        main_input = Input(shape=(max_len, num_features), name='main_input')
        processed = main_input

        processed = Dense(32)(processed)
        processed = BatchNormalization()(processed)
        processed = LeakyReLU()(processed)
        processed = Dropout(0.5)(processed)

        processed = LSTM(64, return_sequences=False, recurrent_dropout=0.5)(processed)

        processed = Dense(32)(processed)
        processed = BatchNormalization()(processed)
        processed = LeakyReLU()(processed)
        processed = Dropout(0.5)(processed)

        act_output = Dense(len(target_chars), activation='softmax', name='act_output')(processed)
        group_output = Dense(len(target_chars_group), activation='softmax', name='group_output')(processed)
        elapsed_time_output = Dense(len(target_chars_time), activation='softmax', name='elapsed_time_output')(processed)
        time_output = Dense(1, activation='sigmoid', name='time_output')(processed)

        model = Model(main_input, [act_output, group_output, elapsed_time_output, time_output])
        model.compile(loss={'act_output': 'categorical_crossentropy',
                            'group_output': 'categorical_crossentropy',
                            'elapsed_time_output': 'categorical_crossentropy',
                            'time_output': 'mae'},
                      # loss_weights=[0.5, 0.5, 0.0],
                      optimizer='adam')
        return model

    @staticmethod
    def _train_model(model, checkpoint_name, X, y_a, y_t, y_y, y_g):
        model_checkpoint = ModelCheckpoint(checkpoint_name, save_best_only=True)
        early_stopping = EarlyStopping(monitor='val_loss', patience=5)

        model.fit(X, {'act_output': y_a,
                      'time_output': y_t,
                      'elapsed_time_output': y_y,
                      'group_output': y_g},
                  validation_split=validation_split,
                  verbose=2,
                  callbacks=[early_stopping, model_checkpoint],
                  epochs=epochs)

    @staticmethod
    def train(log_name, models_folder, use_old_model):
        lines = []
        lines_group = []
        lines_time = []
        timeseqs = []
        timeseqs2 = []
        lastcase = ''
        line = ''
        line_group = ''
        line_time = ''
        first_line = True
        times = []
        times2 = []
        difflist = []
        numlines = 0
        casestarttime = None
        lasteventtime = None

        r = 3

        csvfile = open(shared_variables.data_folder + '%s.csv' % log_name, 'r')
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader, None)  # skip the headers

        for row in spamreader:
            t1 = time.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            if row[0] != lastcase:
                lastevent = t1
                lastcase = row[0]
            if row[1] != '0':
                t2 = datetime.fromtimestamp(time.mktime(t1)) - datetime.fromtimestamp(time.mktime(lastevent))
                tdiff = 86400 * t2.days + t2.seconds
            else:
                tdiff = 0
            difflist.append(tdiff)
            lastevent = t1

        difflist = [int(i) for i in difflist]
        maxdiff = max(difflist)
        difflist[np.argmax(difflist)] -= 1e-8
        diff = maxdiff / r
        # difflist.sort()
        # mediandiff = np.percentile(difflist, 50)
        # diff = mediandiff / r

        # print(maxdiff)
        # print(mediandiff)
        csvfile.seek(0)
        next(spamreader, None)  # skip the headers

        line_index = 0
        for row in spamreader:
            t = time.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            if row[0] != lastcase:
                casestarttime = t
                lasteventtime = t
                lastcase = row[0]
                if not first_line:
                    lines.append(line)
                    lines_group.append(line_group)
                    lines_time.append(line_time)
                    timeseqs.append(times)
                    timeseqs2.append(times2)
                line = ''
                line_group = ''
                line_time = ''
                times = []
                times2 = []
                numlines += 1
            line += get_unicode_from_int(row[1])
            line_group += get_unicode_from_int(row[3])

            # if (difflist[line_index] / diff) <= r:
            #     line_time += get_unicode_from_int(int(int(row[4]) / diff))
            # else:
            line_time += get_unicode_from_int(int(difflist[line_index] / diff))
            timesincelastevent = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(
                time.mktime(lasteventtime))
            timesincecasestart = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(
                time.mktime(casestarttime))
            timediff = 86400 * timesincelastevent.days + timesincelastevent.seconds
            timediff2 = 86400 * timesincecasestart.days + timesincecasestart.seconds
            times.append(timediff)
            times2.append(timediff2)
            lasteventtime = t
            first_line = False
            line_index += 1
        # add last case
        lines.append(line)
        lines_group.append(line_group)
        lines_time.append(line_time)
        timeseqs.append(times)
        timeseqs2.append(times2)
        numlines += 1

        divisor = np.max([item for sublist in timeseqs for item in sublist])
        print('divisor: {}'.format(divisor))
        divisor2 = np.max([item for sublist in timeseqs2 for item in sublist])
        print('divisor2: {}'.format(divisor2))

        elements_per_fold = int(round(numlines / 3))
        fold1 = lines[:elements_per_fold]
        fold1_group = lines_group[:elements_per_fold]
        fold1_time = lines_time[:elements_per_fold]

        fold2 = lines[elements_per_fold:2 * elements_per_fold]
        fold2_group = lines_group[elements_per_fold:2 * elements_per_fold]
        fold2_time = lines_time[elements_per_fold:2 * elements_per_fold]

        lines = fold1 + fold2
        lines_group = fold1_group + fold2_group
        lines_time = fold1_time + fold2_time

        lines = map(lambda x: x + '!', lines)
        maxlen = max(map(lambda x: len(x), lines))

        chars = map(lambda x: set(x), lines)
        chars = list(set().union(*chars))
        chars.sort()
        target_chars = copy.copy(chars)
        chars.remove('!')
        print('total chars: {}, target chars: {}'.format(len(chars), len(target_chars)))
        char_indices = dict((c, i) for i, c in enumerate(chars))
        target_char_indices = dict((c, i) for i, c in enumerate(target_chars))

        # lines_group = map(lambda x: x+'!', lines_group)

        chars_group = map(lambda x: set(x), lines_group)
        chars_group = list(set().union(*chars_group))
        chars_group.sort()
        target_chars_group = copy.copy(chars_group)
        # chars_group.remove('!')
        print('total groups: {}, target groups: {}'.format(len(chars_group), len(target_chars_group)))
        char_indices_group = dict((c, i) for i, c in enumerate(chars_group))
        target_char_indices_group = dict((c, i) for i, c in enumerate(target_chars_group))

        chars_time = map(lambda x: set(x), lines_time)
        chars_time = list(set().union(*chars_time))
        chars_time.sort()
        target_chars_time = copy.copy(chars_time)

        print('total times: {}, target times: {}'.format(len(chars_time), len(target_chars_time)))
        char_indices_time = dict((c, i) for i, c in enumerate(chars_time))
        target_char_indices_time = dict((c, i) for i, c in enumerate(target_chars_time))

        csvfile = open(shared_variables.data_folder + '%s.csv' % log_name, 'r')
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader, None)  # skip the headers
        lastcase = ''
        line = ''
        line_group = ''
        line_time = ''
        first_line = True
        lines_id = []
        lines = []
        lines_group = []
        lines_time = []
        timeseqs = []  # relative time since previous event
        timeseqs2 = []  # relative time since case start
        timeseqs3 = []  # absolute time of previous event
        timeseqs4 = []  # absolute time of event as a string
        times = []
        times2 = []
        times3 = []
        times4 = []
        numlines = 0
        casestarttime = None
        lasteventtime = None
        line_index = 0
        for row in spamreader:
            t = time.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            if row[0] != lastcase:
                casestarttime = t
                lasteventtime = t
                lastcase = row[0]
                if not first_line:
                    lines.append(line)
                    lines_group.append(line_group)
                    lines_time.append(line_time)
                    timeseqs.append(times)
                    timeseqs2.append(times2)
                    timeseqs3.append(times3)
                    timeseqs4.append(times4)
                lines_id.append(lastcase)
                line = ''
                line_group = ''
                times = []
                times2 = []
                times3 = []
                times4 = []
                numlines += 1
            line += get_unicode_from_int(row[1])
            line_group += get_unicode_from_int(row[3])
            line_time += get_unicode_from_int(int(difflist[line_index] / diff))
            timesincelastevent = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(
                time.mktime(lasteventtime))
            timesincecasestart = datetime.fromtimestamp(time.mktime(t)) - datetime.fromtimestamp(
                time.mktime(casestarttime))
            midnight = datetime.fromtimestamp(time.mktime(t)).replace(hour=0, minute=0, second=0, microsecond=0)
            timesincemidnight = datetime.fromtimestamp(time.mktime(t)) - midnight
            timediff = 86400 * timesincelastevent.days + timesincelastevent.seconds
            timediff2 = 86400 * timesincecasestart.days + timesincecasestart.seconds
            timediff3 = timesincemidnight.seconds
            timediff4 = datetime.fromtimestamp(time.mktime(t)).weekday()
            times.append(timediff)
            times2.append(timediff2)
            times3.append(timediff3)
            times4.append(timediff4)
            lasteventtime = t
            first_line = False
            line_index += 1

        # add last case
        lines.append(line)
        lines_group.append(line_group)
        lines_time.append(line_time)
        timeseqs.append(times)
        timeseqs2.append(times2)
        timeseqs3.append(times3)
        timeseqs4.append(times4)
        numlines += 1

        elements_per_fold = int(round(numlines / 3))

        lines = lines[:-elements_per_fold]
        lines_group = lines_group[:-elements_per_fold]
        lines_time = lines_time[:-elements_per_fold]
        lines_t = timeseqs[:-elements_per_fold]
        lines_t2 = timeseqs2[:-elements_per_fold]
        lines_t3 = timeseqs3[:-elements_per_fold]
        lines_t4 = timeseqs4[:-elements_per_fold]

        step = 1
        sentences = []
        sentences_group = []
        sentences_time = []
        softness = 0
        next_chars = []
        next_chars_group = []
        next_chars_time = []
        lines = map(lambda x: x + '!', lines)
        lines_group = map(lambda x: x + '!', lines_group)
        lines_time = map(lambda x: x + '!', lines_time)

        sentences_t = []
        sentences_t2 = []
        sentences_t3 = []
        sentences_t4 = []
        next_chars_t = []
        for line, line_group, line_time, line_t, line_t2, line_t3, line_t4 in izip(lines, lines_group, lines_time,
                                                                                   lines_t, lines_t2, lines_t3,
                                                                                   lines_t4):
            for i in range(0, len(line), step):
                if i == 0:
                    continue
                sentences.append(line[0: i])
                sentences_group.append(line_group[0:i])
                sentences_time.append(line_time[0:i])
                sentences_t.append(line_t[0:i])
                sentences_t2.append(line_t2[0:i])
                sentences_t3.append(line_t3[0:i])
                sentences_t4.append(line_t4[0:i])
                next_chars.append(line[i])
                next_chars_group.append(line_group[i])
                next_chars_time.append(line_time[i])
                if i == len(line) - 1:  # special case to deal time of end character
                    next_chars_t.append(0)
                else:
                    next_chars_t.append(line_t[i])
        print('nb sequences:', len(sentences))

        print('Vectorization...')
        num_features = len(chars) + len(chars_group) + len(chars_time) + 5
        print('num features: {}'.format(num_features))
        print('MaxLen: ', maxlen)
        X = np.zeros((len(sentences), maxlen, num_features), dtype=np.float32)
        y_a = np.zeros((len(sentences), len(target_chars)), dtype=np.float32)
        y_g = np.zeros((len(sentences), len(target_chars_group)), dtype=np.float32)
        y_t = np.zeros((len(sentences)), dtype=np.float32)
        y_y = np.zeros((len(sentences), len(target_chars_time)), dtype=np.float32)
        for i, sentence in enumerate(sentences):
            leftpad = maxlen - len(sentence)
            next_t = next_chars_t[i]
            sentence_group = sentences_group[i]
            sentence_time = sentences_time[i]
            sentence_t = sentences_t[i]
            sentence_t2 = sentences_t2[i]
            sentence_t3 = sentences_t3[i]
            sentence_t4 = sentences_t4[i]
            for t, char in enumerate(sentence):
                for c in chars:
                    if c == char:
                        X[i, t + leftpad, char_indices[c]] = 1
                for g in chars_group:
                    if g == sentence_group[t]:
                        X[i, t + leftpad, len(chars) + char_indices_group[g]] = 1
                for y in chars_time:
                    if y == sentence_time[t]:
                        X[i, t + leftpad, len(chars) + len(chars_group) + char_indices_time[y]] = 1
                X[i, t + leftpad, len(chars) + len(chars_group) + len(chars_time)] = t + 1
                X[i, t + leftpad, len(chars) + len(chars_group) + len(chars_time) + 1] = sentence_t[t] / divisor
                X[i, t + leftpad, len(chars) + len(chars_group) + len(chars_time) + 2] = sentence_t2[t] / divisor2
                X[i, t + leftpad, len(chars) + len(chars_group) + len(chars_time) + 3] = sentence_t3[t] / 86400
                X[i, t + leftpad, len(chars) + len(chars_group) + len(chars_time) + 4] = sentence_t4[t] / 7
            for c in target_chars:
                if c == next_chars[i]:
                    y_a[i, target_char_indices[c]] = 1 - softness
                else:
                    y_a[i, target_char_indices[c]] = softness / (len(target_chars) - 1)
            for g in target_chars_group:
                if g == next_chars_group[i]:
                    y_g[i, target_char_indices_group[g]] = 1 - softness
                else:
                    y_g[i, target_char_indices_group[g]] = softness / (len(target_chars_group) - 1)
            for y in target_chars_time:
                if y == next_chars_time[i]:
                    y_y[i, target_char_indices_time[y]] = 1 - softness
                else:
                    y_y[i, target_char_indices_time[y]] = softness / (len(target_chars_time) - 1)
            y_t[i] = next_t / divisor

        for fold in range(folds):
            model = TrainCFRT._build_model(maxlen, num_features, target_chars, target_chars_time, target_chars_group,
                                           use_old_model)
            checkpoint_name = create_checkpoints_path(log_name, models_folder, fold, 'CFRT')
            TrainCFRT._train_model(model, checkpoint_name, X, y_a, y_t, y_y, y_g)
