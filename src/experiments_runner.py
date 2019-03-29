import sys

import keras.backend as K
import tensorflow as tf

from evaluator import Evaluator
from train_cf import TrainCF
from train_cfr import TrainCFR
from train_cfrt import TrainCFRT


class ExperimentRunner:
    _log_names = [
        #'10x5_1S',
        #'10x5_1W',
        # '10x5_3S',
        #'10x5_3W',
        #'5x5_1W',
        #'5x5_1S',
        #'5x5_3W',
        #'5x5_3S',
        #'10x20_1W',
        #'10x20_1S',
        #'10x20_3W',
        # '10x20_3S',
        #'10x2_1W',
        #'10x2_1S',
        #'10x2_3W',
        # '10x2_3S',
        #'50x5_1W',
        # '50x5_1S',
        #'50x5_3W',
        # '50x5_3S',
        #'Hospital_log',
        'BPI2017',
        #'SepsisCases_log'
        #'BPI2012'
        #'SepsisCases_log_big'
    ]

    _models_folder = 'final_experiments'

    def __init__(self):
        pass

    @staticmethod
    def _run_single_experiment(log_name, folds, use_time):
        print(log_name)
        if use_time:
            TrainCFRT.train(log_name, ExperimentRunner._models_folder, folds)
            try:
                Evaluator.evaluate_time(log_name, ExperimentRunner._models_folder, folds)
            except:
                Evaluator.evaluate_time(log_name, ExperimentRunner._models_folder, folds)

        else:
            #TrainCF.train(log_name, ExperimentRunner._models_folder, folds)
            #TrainCFR.train(log_name, ExperimentRunner._models_folder, folds)
            try:
                Evaluator.evaluate_all(log_name, ExperimentRunner._models_folder, folds)
            except:
                Evaluator.evaluate_all(log_name, ExperimentRunner._models_folder, folds)

    @staticmethod
    def run_experiments(input_log_name=None):
        folds = 1
        use_time = True
        config = tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=4,
                                allow_soft_placement=True)
        session = tf.Session(config=config)
        K.set_session(session)

        if input_log_name is not None:
            ExperimentRunner._run_single_experiment(input_log_name, folds, use_time)
        else:
            for log_name in ExperimentRunner._log_names:
                ExperimentRunner._run_single_experiment(log_name, folds, use_time)


if __name__ == "__main__":
    log_name = ''
    if len(sys.argv) > 1:
        log_name = sys.argv[1]
    ExperimentRunner.run_experiments(input_log_name=None)
