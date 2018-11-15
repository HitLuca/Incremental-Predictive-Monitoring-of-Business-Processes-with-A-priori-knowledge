"""
This file was created to manage running of experiments.

## settings are in the shared variables file
"""

import train_cf
import train_cfr
import tensorflow as tf
import keras.backend as K

from inference_algorithms.used_algorithms import _6_evaluate_baseline_SUFFIX_only, \
    _6_evaluate_baseline_SUFFIX_and_group, _11_cycl_pro_SUFFIX_only, _11_cycl_pro_SUFFIX_resource_LTL, \
    _11_cycl_pro_SUFFIX_declare_smart_queue


def train_and_evaluate_cf(log_name):
    train_cf.train(log_name)
    _6_evaluate_baseline_SUFFIX_only.run_experiments(log_name)
    _11_cycl_pro_SUFFIX_only.run_experiments(log_name)


def train_and_evaluate_cfr(log_name):
    train_cfr.train(log_name)
    _6_evaluate_baseline_SUFFIX_and_group.run_experiments(log_name)
    _11_cycl_pro_SUFFIX_resource_LTL.run_experiments(log_name)
    _11_cycl_pro_SUFFIX_declare_smart_queue.run_experiments(log_name)


log_names = ['10x5_1S', '10x5_1W', '10x5_3S',
             '10x5_3W', '5x5_1W', '5x5_1S', '5x5_3W', '5x5_3S', '10x20_1W', '10x20_1S',
             '10x20_3W', '10x20_3S', '10x2_1W', '10x2_1S', '10x2_3W', '10x2_3S', '50x5_1W', '50x5_1S', '50x5_3W',
             '50x5_3S']
            # , 'BPI2017_50k']


def main():
    config = tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=4, allow_soft_placement=True)
    session = tf.Session(config=config)
    K.set_session(session)

    for log_name in log_names:
        print(log_name)
        train_and_evaluate_cf(log_name)
        train_and_evaluate_cfr(log_name)
        print()


if __name__ == "__main__":
    main()
