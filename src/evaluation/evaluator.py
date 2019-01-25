from evaluation.server_replayer import ServerReplayer
from evaluation.inference_algorithms import baseline_1_cf, baseline_1_cfr, baseline_1_cfrt, baseline_2_cf, \
    baseline_2_cfr
from shared_variables import folds


class Evaluator:
    def __init__(self, port, python_port):
        self._server_replayer = ServerReplayer(port, python_port)

    def _start_server_and_evaluate(self, evaluation_algorithm, log_name, models_folder, fold):
        self._server_replayer.start_server()
        evaluation_algorithm.run_experiments(self._server_replayer, log_name, models_folder, fold)
        self._server_replayer.stop_server()

    def evaluate_all(self, log_name, models_folder):
        for fold in range(folds):
            print('baseline_1 CF')
            self._start_server_and_evaluate(baseline_1_cf, log_name, models_folder, fold)
            print('baseline_2 CF')
            self._start_server_and_evaluate(baseline_2_cf, log_name, models_folder, fold)
            print('baseline_1 CFR')
            self._start_server_and_evaluate(baseline_1_cfr, log_name, models_folder, fold)
            print('baseline_2 CFR')
            self._start_server_and_evaluate(baseline_2_cfr, log_name, models_folder, fold)
            # print('new method')
            # self._start_server_and_evaluate(new_method_cfr, log_name, models_folder, fold)

    def evaluate_time(self, log_name, models_folder):
        for fold in range(folds):
            print('baseline_1 CFRT')
            self._start_server_and_evaluate(baseline_1_cfrt, log_name, models_folder, fold)
