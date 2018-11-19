"""
This file was created to manage running of experiments.

## settings are in the shared variables file
"""
import train_cf
import train_cfr
import tensorflow as tf
import keras.backend as K

from inference_algorithms.used_algorithms import \
    _6_evaluate_baseline_SUFFIX_only as baseline_1_cf, \
    _6_evaluate_baseline_SUFFIX_and_group as baseline_1_cfr, \
    _11_cycl_pro_SUFFIX_only as baseline_2_cf, \
    _11_cycl_pro_SUFFIX_resource_LTL as baseline_2_cfr, \
    _11_cycl_pro_SUFFIX_declare_smart_queue as new_approach_cfr


def evaluate_baselines_cf(log_name):
    baseline_1_cf.run_experiments(log_name)
    baseline_2_cf.run_experiments(log_name)


def evaluate_baselines_cfr(log_name):
    baseline_1_cfr.run_experiments(log_name)
    baseline_2_cfr.run_experiments(log_name)


def evaluate_new_approach_cfr(log_name):
    new_approach_cfr.run_experiments(log_name)


log_names = ['10x5_1S', '10x5_1W', '10x5_3S',
             '10x5_3W', '5x5_1W', '5x5_1S', '5x5_3W', '5x5_3S', '10x20_1W', '10x20_1S',
             '10x20_3W', '10x20_3S', '10x2_1W', '10x2_1S', '10x2_3W', '10x2_3S', '50x5_1W', '50x5_1S', '50x5_3W',
             '50x5_3S']  # , 'BPI2017_50k']


def main():
    config = tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=4, allow_soft_placement=True)
    session = tf.Session(config=config)
    K.set_session(session)

    for log_name in log_names:
        print(log_name)
        train_cf.train(log_name)
        evaluate_baselines_cf(log_name)
        print

    for log_name in log_names:
        print(log_name)
        train_cfr.train(log_name)
        evaluate_baselines_cfr(log_name)
        print

    for log_name in log_names:
        print(log_name)
        evaluate_new_approach_cfr(log_name)
        print


if __name__ == "__main__":
    main()
