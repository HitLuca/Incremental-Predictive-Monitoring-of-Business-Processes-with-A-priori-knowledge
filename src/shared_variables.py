"""
This file was created in order to bring
common variables and functions into one file to make
code more clear

"""

ascii_offset = 161
beam_size = 3
prefix_size_pred_to = None
prefix_size_pred_from = None
base_folderpath = 'output_files/final_experiments/models/'


def get_unicode_from_int(ch):
    return unichr(int(ch) + ascii_offset)


def get_int_from_unicode(unch):
    return int(ord(unch)) - ascii_offset


# noinspection PyShadowingNames
def activate_settings(log_number, formula_type=''):
    eventlog = ''
    model_CF_filepath = ''
    model_CFR_filepath = ''
    formula = ''
    prefix_size_pred_from = 0
    prefix_size_pred_to = 0

    if log_number == 1:
        eventlog = '10x5_1S'
        model_CF_filepath = 'model_003-1.067.h5'
        model_CFR_filepath = 'model_026-1.641.h5'
        formula = " []( ( \"6\" -> <>( \"3\" ) ) )  /\ <>\"6\" "
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 2:
        eventlog = '10x5_1W'
        model_CF_filepath = 'model_18-1.07.h5'
        model_CFR_filepath = 'model_22-1.71.h5'
        formula = "<>(\"6\")"

        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 3:
        eventlog = '10x5_3S'
        model_CF_filepath = 'model_001-1.868.h5'
        model_CFR_filepath = 'model_21-1.44.h5'
        formula = " []( ( \"6\" -> <>( \"1\" ) ) )  /\ <>\"6\" /\  []( ( \"8\" -> <>( \"1\" ) ) )  /\ <>\"8\" /\ "
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 4:
        eventlog = '10x5_3W'
        model_CF_filepath = 'model_05-1.10.h5'
        model_CFR_filepath = 'model_11-1.55.h5'
        formula = "<>(\"8\") /\ <>(\"7\")"
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 5:
        eventlog = '5x5_1W'
        model_CF_filepath = 'model_23-1.12.h5'
        model_CFR_filepath = 'model_15-1.69.h5'
        formula = "<>(\"3\")"

    elif log_number == 6:
        eventlog = '5x5_1S'
        model_CF_filepath = 'model_17-1.16.h5'
        model_CFR_filepath = 'model_35-1.83.h5'
        formula = " []( ( \"3\" -> <>( \"4\" ) ) )  /\ <>\"3\" "
        prefix_size_pred_from = 2
        prefix_size_pred_to = 6

    elif log_number == 7:
        eventlog = '5x5_3W'
        model_CF_filepath = 'model_18-1.23.h5'
        model_CFR_filepath = 'model_10-1.77.h5'
        formula = "<>(\"4\") /\ <>(\"3\")"
        prefix_size_pred_from = 2
        prefix_size_pred_to = 4

    elif log_number == 8:
        eventlog = '5x5_3S'
        model_CF_filepath = 'model_39-1.32.h5'
        model_CFR_filepath = 'model_31-1.73.h5'
        formula = " []( ( \"4\" -> <>( \"3\" ) ) )  /\ <>\"4\" /\  []( ( \"3\" -> <>( \"0\" ) ) )  /\ <>\"3\" /\ "
        prefix_size_pred_from = 2
        prefix_size_pred_to = 4

    elif log_number == 9:
        eventlog = '10x20_1W'
        model_CF_filepath = 'model_04-1.09.h5'
        model_CFR_filepath = 'model_03-1.64.h5'
        formula = "<>(\"9\")"
        prefix_size_pred_from = 2
        prefix_size_pred_to = 6

    elif log_number == 10:
        eventlog = '10x20_1S'
        model_CF_filepath = 'model_002-0.271.h5'
        model_CFR_filepath = 'model_005-1.480.h5'
        if formula_type == 'STRONG':
            formula = " []( ( \"8\" -> <>( \"9\" ) ) )  /\ <>\"8\" "
        elif formula_type == 'WEAK':
            formula = "<>(\"9\")"

        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 11:
        eventlog = '10x20_3W'
        model_CF_filepath = 'model_06-1.17.h5'
        model_CFR_filepath = 'model_05-1.63.h5'
        formula = "<>(\"9\") /\ <>(\"6\") /\ <>(\"8\")"
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 12:
        eventlog = '10x20_3S'
        model_CF_filepath = 'model_24-1.09.h5'
        model_CFR_filepath = 'model_06-1.54.h5'
        formula = "[]( ( \"9\" -> <>( \"7\" ) ) )  /\ <>\"9\" /\  []( ( \"8\" -> <>( \"6\" ) ) )  /\ <>\"8\" /\  []( " \
                  "( \"7\" -> <>( \"5\" ) ) )  /\ <>\"7\" "
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 13:
        eventlog = '10x2_1W'
        model_CF_filepath = 'model_70-1.14.h5'
        model_CFR_filepath = 'model_21-1.77.h5'
        formula = "<>(\"2\")"
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 14:
        eventlog = '10x2_1S'
        model_CF_filepath = 'model_02-1.83.h5'
        model_CFR_filepath = 'model_01-1.94.h5'
        formula = " []( ( \"6\" -> <>( \"2\" ) ) )  /\ <>\"6\""
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 15:
        eventlog = '10x2_3W'
        model_CF_filepath = 'model_19-1.12.h5'
        model_CFR_filepath = 'model_24-1.54.h5'
        formula = "<>(\"8\") /\ <>(\"7\")"
        prefix_size_pred_from = 5
        prefix_size_pred_to = 7

    elif log_number == 16:
        eventlog = '10x2_3S'
        model_CF_filepath = 'model_09-1.56.h5'
        model_CFR_filepath = 'model_03-1.78.h5'
        formula = " []( ( \"9\" -> <>( \"3\" ) ) )  /\ <>\"9\" /\  []( ( \"7\" -> <>( \"3\" ) ) )  /\ <>\"7\""
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 17:
        eventlog = '50x5_1W'
        model_CF_filepath = 'model_01-1.25.h5'
        model_CFR_filepath = 'model_01-1.58.h5'
        formula = "<>(\"7\")"
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 18:
        eventlog = '50x5_1S'
        model_CF_filepath = 'model_01-1.21.h5'
        model_CFR_filepath = 'model_01-1.45.h5'
        formula = " []( ( \"7\" -> <>( \"8\" ) ) )  /\ <>\"7\""
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 19:
        eventlog = '50x5_3W'
        model_CF_filepath = 'model_09-1.07.h5'
        model_CFR_filepath = 'model_02-1.28.h5'
        formula = "<>(\"9\") /\ <>(\"7\")"
        prefix_size_pred_from = 3
        prefix_size_pred_to = 7

    elif log_number == 20:
        eventlog = '50x5_3S'
        model_CF_filepath = 'model_04-1.38.h5'
        model_CFR_filepath = 'model_07-1.52.h5'
        formula = " []( ( \"9\" -> <>( \"7\" ) ) )  /\ <>\"9\" /\  []( ( \"8\" -> <>( \"7\" ) ) )  /\ <>\"8\""
        prefix_size_pred_from = 6
        prefix_size_pred_to = 7

    elif log_number == 21:
        eventlog = 'BPI2017_50k'
        model_CF_filepath = ''
        model_CFR_filepath = 'model_14-2.26.h5'
        if formula_type == 'STRONG':
            formula = " []( ( \"17\" -> <>( \"18\" ) ) )  /\ <>\"17\""
        elif formula_type == 'WEAK':
            formula = "<>(\"17\")"

        prefix_size_pred_from = 6
        prefix_size_pred_to = 9

    path_to_model_file_CF = base_folderpath + 'CF/' + eventlog + model_CF_filepath
    path_to_model_file_CFR = base_folderpath + 'CFR/' + eventlog + model_CFR_filepath
    path_to_declare_model_file = 'declare_models/final_experiments/' + eventlog + '.xml'

    return eventlog, path_to_model_file_CF, path_to_model_file_CFR, path_to_declare_model_file, beam_size, \
           prefix_size_pred_from, prefix_size_pred_to, formula
