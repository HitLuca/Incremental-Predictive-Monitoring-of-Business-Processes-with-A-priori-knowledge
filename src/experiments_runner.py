import keras.backend as K
import tensorflow as tf

from train_cf import TrainCF
from train_cfr import TrainCFR
from evaluator import Evaluator


class ExperimentRunner:
    _log_names = [
        '10x5_1S', '10x5_1W', '10x5_3S',
        '10x5_3W',
        '5x5_1W', '5x5_1S', '5x5_3W',
        '5x5_3S', '10x20_1W', '10x20_1S',
        '10x20_3W', '10x20_3S', '10x2_1W',
        '10x2_1S', '10x2_3W',
        '10x2_3S', '50x5_1W', '50x5_1S', '50x5_3W',
        '50x5_3S'
    ]  # , 'BPI2017_50k']

    _models_folder = 'final_experiments_5'

    def __init__(self):
        pass

    @staticmethod
    def run_experiments():
        folds = 3
        config = tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=4,
                                allow_soft_placement=True)
        session = tf.Session(config=config)
        K.set_session(session)

        for log_name in ExperimentRunner._log_names:
            print(log_name)
            TrainCF.train(log_name, ExperimentRunner._models_folder, folds)
            TrainCFR.train(log_name, ExperimentRunner._models_folder, folds)
            # try:
            #     Evaluator.evaluate_all(log_name, ExperimentRunner._models_folder, folds)
            # except:
            #     Evaluator.evaluate_all(log_name, ExperimentRunner._models_folder, folds)


if __name__ == "__main__":
    ExperimentRunner.run_experiments()
