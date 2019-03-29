import subprocess

from inference_algorithms import \
    _6_evaluate_baseline_SUFFIX_only as baseline_1_cf, \
    _6_evaluate_baseline_SUFFIX_and_group as baseline_1_cfr, \
    _6_evaluate_baseline_SUFFIX_group_and_elapsed_time as baseline_1_cfrt, \
    _6_cycl_pro_evaluate_baseline_SUFFIX_group_and_elapsed_time as baseline_1_cfrt_cycle, \
    _11_cycl_pro_SUFFIX_only as baseline_2_cf, \
    _11_cycl_pro_SUFFIX_resource_LTL as baseline_2_cfr, \
    _11_cycl_pro_SUFFIX_declare_smart_queue as new_approach_cfr, \
    _11_cycl_pro_SUFFIX_elapsed_time_declare_smart_queue as new_approach_cfrt


class Evaluator:
    _server_start_instructions = ['java', '-jar', '../LTLCheckForTraces.jar']

    def __init__(self):
        pass

    @staticmethod
    def _start_server_and_evaluate(evaluation, log_name, models_folder, fold):
        p = subprocess.Popen(Evaluator._server_start_instructions)
        evaluation.run_experiments(log_name, models_folder, fold)
        p.terminate()
        p.wait()

    @staticmethod
    def evaluate_all(log_name, models_folder, folds):
        for fold in range(folds):
            # print('baseline_1 CF')
            # Evaluator._start_server_and_evaluate(baseline_1_cf, log_name, models_folder, fold)
            # print('baseline_2 CF')
            # Evaluator._start_server_and_evaluate(baseline_2_cf, log_name, models_folder, fold)
            # print('baseline_1 CFR')
            # Evaluator._start_server_and_evaluate(baseline_1_cfr, log_name, models_folder, fold)
            # print('baseline_2 CFR')
            # Evaluator._start_server_and_evaluate(baseline_2_cfr, log_name, models_folder, fold)
            print('new method')
            Evaluator._start_server_and_evaluate(new_approach_cfr, log_name, models_folder, fold)

    @staticmethod
    def evaluate_time(log_name, models_folder, folds):
        for fold in range(folds):
            print('baseline_1 CFRT')
            Evaluator._start_server_and_evaluate(baseline_1_cfrt, log_name, models_folder, fold)
            #print('baseline_1 CFRT CYCLE')
            #Evaluator._start_server_and_evaluate(baseline_1_cfrt_cycle, log_name, models_folder, fold)
            print('new method CFRT')
            Evaluator._start_server_and_evaluate(new_approach_cfrt, log_name, models_folder, fold)