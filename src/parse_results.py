import csv

import numpy as np
from matplotlib import pyplot as plt


class ResultParser:
    _log_names = ['10x2_1W', '10x2_3W', '10x2_1S', '10x2_3S', '10x5_1W', '10x5_3W', '10x5_1S', '10x5_3S', '10x20_1W',
                  '10x20_3W', '10x20_1S', '10x20_3S', '5x5_1W', '5x5_3W', '5x5_1S', '5x5_3S', '50x5_1W', '50x5_3W',
                  '50x5_1S', '50x5_3S']

    _headers = ['E1_CF', 'E1_CFR_1', 'E1_CFR_2', 'E2_CF', 'E2_CFR_1', 'E2_CFR_2', 'E3_CFR_1', 'E3_CFR_2']
    _metrics = ['baseline', 'LTL', 'declare']

    _model_types = ['CF', 'CFR']

    # <editor-fold desc="reference_table">
    _reference_table = np.array(
        [[0.693, 0.742, 0.511, 0.658, 0.804, 0.729, 0.390, 0.765, 0.727, 0.784, 0.827, 0.849, 0.618,
          0.729, 0.727, 0.409, 0.553, 0.314, 0.231, 0.623],
         [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
          0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
         [0.643, 0.806, 0.258, 0.629, 0.810, 0.723, 0.695, 0.831, 0.864, 0.761, 0.784, 0.774, 0.645,
          0.749, 0.655, 0.806, 0.735, 0.506, 0.466, 0.802],
         [0.674, 0.682, 0.803, 0.793, 0.800, 0.605, 0.700, 0.741, 0.579, 0.583, 0.608, 0.566, 0.677,
          0.574, 0.642, 0.644, 0.642, 0.308, 0.377, 0.803],
         [0.649, 0.742, 0.682, 0.682, 0.803, 0.719, 0.479, 0.769, 0.909, 0.784, 0.884, 0.556, 0.616,
          0.729, 0.726, 0.413, 0.746, 0.674, 0.874, 0.732],
         [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
          0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
         [0.665, 0.806, 0.536, 0.662, 0.813, 0.723, 0.720, 0.846, 0.855, 0.723, 0.884, 0.620, 0.639,
          0.750, 0.691, 0.806, 0.707, 0.819, 0.825, 0.789],
         [0.640, 0.682, 0.760, 0.826, 0.800, 0.605, 0.717, 0.761, 0.579, 0.571, 0.627, 0.449, 0.684,
          0.574, 0.650, 0.643, 0.561, 0.514, 0.623, 0.799],
         [0.646, 0.803, 0.695, 0.667, 0.780, 0.831, 0.802, 0.849, 0.864, 0.838, 0.884, 0.000, 0.601,
          0.754, 0.718, 0.846, 0.697, 0.735, 0.870, 0.811],
         [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
          0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
         [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
          0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
         [0.649, 0.679, 0.763, 0.833, 0.790, 0.824, 0.792, 0.761, 0.575, 0.738, 0.704, 0.000, 0.785,
          0.758, 0.763, 0.679, 0.687, 0.742, 0.875, 0.815]]).T

    # </editor-fold>

    def __init__(self):
        pass

    @staticmethod
    def _parse_log(filepath, two_predictions=False):
        label_1 = 'Damerau-Levenshtein'
        label_2 = 'Damerau-Levenshtein Resource'

        if two_predictions:
            scores = [[], []]
        else:
            scores = [[]]

        with open(filepath, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='|')
            csv_headers = next(csv_reader)

            for row in csv_reader:
                score_1 = float(row[csv_headers.index(label_1)])
                scores[0].append(score_1)

                if two_predictions:
                    score_2 = float(row[csv_headers.index(label_2)])
                    scores[1].append(score_2)

        scores = np.mean(np.array(scores), -1)
        return scores

    @staticmethod
    def _populate_table(table, scores, log_name, metric, model_type):
        row = ResultParser._log_names.index(log_name)
        column = ResultParser._metrics.index(metric) * len(
            ResultParser._model_types) * 2 + ResultParser._model_types.index(model_type) * len(
            ResultParser._model_types)

        table[row, column] = scores[0]
        if scores.shape[0] == 2:
            table[row, column + 1] = scores[1]

    @staticmethod
    def _print_latex_table(populated_table):
        print('\\begin{tabular}{|l||cccc||cccc||cccc|}')
        print('\\hline')
        print('& '),
        for i, metric in enumerate(ResultParser._metrics):
            print('\\multicolumn{4}{|c|}{\\textbf{' + metric + '}}'),
            if i != len(ResultParser._metrics) - 1:
                print(' & '),
            else:
                print('\\\\')
        print('\\hline\\hline')
        for i, log_name in enumerate(ResultParser._log_names):
            print(log_name.replace('_', '\_') + ' & '),
            for j, score in enumerate(populated_table[i]):
                print('%.2f' % score),
                if j != populated_table.shape[1] - 1:
                    print(' & '),
                else:
                    print('\\\\')
        print('\\hline')
        print('\\end{tabular}')

    @staticmethod
    def _show_comparison_image(populated_table, reference_table):
        indexes_to_keep = [0, 2, 3, 4, 6, 7, 10, 11]

        populated_table = populated_table[:, indexes_to_keep]
        reference_table = reference_table[:, indexes_to_keep]

        improvement_percentage = (1.0 * np.count_nonzero(populated_table > reference_table) / np.count_nonzero(
            populated_table)) * 100.0

        populated_indexes = np.where(populated_table > 0)
        mean_improvement = float(np.mean(populated_table[populated_indexes] - reference_table[populated_indexes]))
        sum_improvement = float(np.sum(populated_table[populated_indexes] - reference_table[populated_indexes]))

        plt.subplots(1, 2)
        plt.subplot(1, 2, 1)
        plt.title('better performance (%.2f' % improvement_percentage + '%)')
        binary_image = np.zeros(populated_table.shape)
        binary_image[populated_table == 0] = -1.0
        binary_image[populated_table > reference_table] = 1.0
        plt.imshow(binary_image, cmap='hot')
        plt.yticks(range(len(ResultParser._log_names)), ResultParser._log_names)
        plt.xticks(range(len(ResultParser._headers)), ResultParser._headers, rotation=90)

        plt.subplot(1, 2, 2)
        plt.title('comparison (mean:%.2f, sum:%.2f' % (mean_improvement, sum_improvement) + ')')
        gradient_image = populated_table - reference_table
        gradient_image[populated_table == 0] = 0
        plt.imshow(gradient_image, vmin=-1, vmax=1,
                   cmap=plt.cm.seismic)
        plt.yticks(range(len(ResultParser._log_names)), ResultParser._log_names)
        plt.xticks(range(len(ResultParser._headers)), ResultParser._headers, rotation=90)
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    @staticmethod
    def _load_table(folderpath, folds):
        table_folds = []
        for fold in range(folds):
            fold_table = np.zeros(
                (len(ResultParser._log_names), len(ResultParser._metrics) * len(ResultParser._model_types) * 2))

            for log_name in ResultParser._log_names:
                for metric in ResultParser._metrics:
                    for model_type in ResultParser._model_types:
                        if metric == 'declare' and model_type == 'CF':
                            continue
                        filepath = folderpath + str(
                            fold) + '/results/' + metric + '/' + log_name + '_' + model_type + '.csv'
                        try:
                            scores = ResultParser._parse_log(filepath, model_type == 'CFR')
                            ResultParser._populate_table(fold_table, scores, log_name, metric, model_type)
                        except:
                            pass
            table_folds.append(fold_table)
        populated_table = np.mean(table_folds, axis=0)
        return populated_table

    @staticmethod
    def _load_table_no_folds(folderpath):
        populated_table = np.zeros(
            (len(ResultParser._log_names), len(ResultParser._metrics) * len(ResultParser._model_types) * 2))

        for log_name in ResultParser._log_names:
            for metric in ResultParser._metrics:
                for model_type in ResultParser._model_types:
                    if metric == 'declare' and model_type == 'CF':
                        continue
                    filepath = folderpath + '/results/' + metric + '/' + log_name + '_' + model_type + '.csv'
                    try:
                        scores = ResultParser._parse_log(filepath, model_type == 'CFR')
                        ResultParser._populate_table(populated_table, scores, log_name, metric, model_type)
                    except:
                        pass
        return populated_table

    @staticmethod
    def parse_and_compare_with_reference(target_table_folderpath, reference_table_folderpath=None, folds=3):
        if reference_table_folderpath is None:
            reference_table = ResultParser._reference_table
        elif reference_table_folderpath == 'zero':
            reference_table = np.zeros(
                (len(ResultParser._log_names), len(ResultParser._metrics) * len(ResultParser._model_types) * 2))
        else:
            reference_table = ResultParser._load_table(reference_table_folderpath, folds)
        target_table = ResultParser._load_table(target_table_folderpath, folds)

        ResultParser._show_comparison_image(target_table, reference_table)
        ResultParser._print_latex_table(target_table)


if __name__ == "__main__":
    final_experiments = 'output_files/final_experiments/'
    folds = 3
    ResultParser.parse_and_compare_with_reference(final_experiments, 'zero', folds)
