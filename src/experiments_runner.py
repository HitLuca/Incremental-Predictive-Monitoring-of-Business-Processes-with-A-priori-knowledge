import sys

import keras.backend as K
import tensorflow as tf

from evaluator import Evaluator
from train_cf import TrainCF
from train_cfr import TrainCFR
from train_cfrt import TrainCFRT

use_old_model = False


class ExperimentRunner:

    _log_names = [
        '10x5_1S',
        '10x5_1W',
        '10x5_3S',
        '10x5_3W',
        '5x5_1W',
        '5x5_1S',
        '5x5_3W',
        '5x5_3S',
        '10x20_1W',
        '10x20_1S',
        '10x20_3W',
        '10x20_3S',
        '10x2_1W',
        '10x2_1S',
        '10x2_3W',
        '10x2_3S',
        '50x5_1W',
        '50x5_1S',
        '50x5_3W',
        '50x5_3S'
    ]

    _models_folder = 'final_experiments'

    def __init__(self):
        pass

    @staticmethod
    def _run_single_experiment(log_name, use_time, use_old_model):
        print(log_name)
        if use_time:
            TrainCFRT.train(log_name, ExperimentRunner._models_folder, use_old_model)
            try:
                Evaluator.evaluate_time(log_name, ExperimentRunner._models_folder)
            except:
                Evaluator.evaluate_time(log_name, ExperimentRunner._models_folder)

        else:
            TrainCF.train(log_name, ExperimentRunner._models_folder, use_old_model)
            TrainCFR.train(log_name, ExperimentRunner._models_folder, use_old_model)
            try:
                Evaluator.evaluate_all(log_name, ExperimentRunner._models_folder)
            except:
                Evaluator.evaluate_all(log_name, ExperimentRunner._models_folder)

    @staticmethod
    def run_experiments(input_log_name=None, use_old_model=False):
        if use_old_model:
            print('using old model!')
            ExperimentRunner._models_folder = 'old_model'
        else:
            print('using new model!')
            ExperimentRunner._models_folder = 'new_model'

        use_time = False
        config = tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=4,
                                allow_soft_placement=True)
        session = tf.Session(config=config)
        K.set_session(session)

        if input_log_name is not None:
            ExperimentRunner._run_single_experiment(input_log_name, use_time, use_old_model)
        else:
            for log_name in ExperimentRunner._log_names:
                ExperimentRunner._run_single_experiment(log_name, use_time, use_old_model)


if __name__ == "__main__":
    log_name = None
    if len(sys.argv) > 1:
        log_name = sys.argv[1]
        if len(sys.argv) == 3:
            use_old_model = int(sys.argv[2]) == 1
    ExperimentRunner.run_experiments(input_log_name=log_name, use_old_model=use_old_model)
