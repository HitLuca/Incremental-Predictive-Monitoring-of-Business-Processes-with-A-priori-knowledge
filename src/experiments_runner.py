"""
This file was created to manage running of experiments.

## settings are in the shared variables file
"""
import os
import subprocess

import keras.backend as K
import tensorflow as tf

from inference_algorithms.used_algorithms import \
    _6_evaluate_baseline_SUFFIX_only as baseline_1_cf, \
    _6_evaluate_baseline_SUFFIX_and_group as baseline_1_cfr, \
    _11_cycl_pro_SUFFIX_only as baseline_2_cf, \
    _11_cycl_pro_SUFFIX_resource_LTL as baseline_2_cfr

server_start_instructions = ['java', '-jar', '../LTLCheckForTraces.jar']

log_names = ['10x5_1S', '10x5_1W', '10x5_3S', '10x5_3W', '5x5_1W', '5x5_1S', '5x5_3W', '5x5_3S', '10x20_1W', '10x20_1S',
    '10x20_3W', '10x20_3S', '10x2_1W', '10x2_1S', '10x2_3W', '10x2_3S', '50x5_1W', '50x5_1S', '50x5_3W',
    '50x5_3S']  # , 'BPI2017_50k']

devnull = open(os.devnull, 'wb')


def start_server_and_evaluate(evaluation, log_name):
    p = subprocess.Popen(server_start_instructions)
    # p = subprocess.Popen(server_start_instructions, stdout=subprocess.PIPE, stderr=devnull)
    evaluation.run_experiments(log_name)
    p.kill()
    p.wait()


def evaluate_all(log_name):
    print('baseline_1 CF')
    start_server_and_evaluate(baseline_1_cf, log_name)
    print('baseline_2 CF')
    start_server_and_evaluate(baseline_2_cf, log_name)
    print('baseline_1 CFR')
    start_server_and_evaluate(baseline_1_cfr, log_name)
    print('baseline_2 CFR')
    start_server_and_evaluate(baseline_2_cfr, log_name)
    print('new method')
    # start_server_and_evaluate(new_approach_cfr, log_name)


def main():
    config = tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=4, allow_soft_placement=True)
    session = tf.Session(config=config)
    K.set_session(session)

    for log_name in log_names:
        print(log_name)
        # train_cf.train(log_name)
        # train_cfr.train(log_name)
        evaluate_all(log_name)
        print


if __name__ == "__main__":
    main()
