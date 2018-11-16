import csv

import numpy as np
from matplotlib import pyplot as plt

log_names = ['10x2_1W', '10x2_3W', '10x2_1S', '10x2_3S', '10x5_1W', '10x5_3W', '10x5_1S', '10x5_3S', '10x20_1W',
             '10x20_3W', '10x20_1S', '10x20_3S', '5x5_1W', '5x5_3W', '5x5_1S', '5x5_3S', '50x5_1W', '50x5_3W',
             '50x5_1S', '50x5_3S']  # , 'BPI2017_50k']

headers = ['E1_CF', 'E1_CFR_1', 'E1_CFR_2', 'E2_CF', 'E2_CFR_1', 'E2_CFR_2', 'E3_CFR_1', 'E3_CFR_2']
metrics = ['baseline', 'LTL', 'declare']

model_types = ['CF', 'CFR']

# <editor-fold desc="reference_table">
reference_table = np.array([[0.693, 0.742, 0.511, 0.658, 0.804, 0.729, 0.390, 0.765, 0.727, 0.784, 0.827, 0.849, 0.618,
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

def parse_log(filepath, two_predictions=False):
    label_1 = 'Damerau-Levenshtein'
    label_2 = 'Damerau-Levenshtein Resource'

    if two_predictions:
        scores = [[], []]
    else:
        scores = [[]]

    with open(filepath, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='|')
        headers = next(csv_reader)

        for row in csv_reader:
            score_1 = float(row[headers.index(label_1)])
            scores[0].append(score_1)

            if two_predictions:
                score_2 = float(row[headers.index(label_2)])
                scores[1].append(score_2)

    scores = np.mean(np.array(scores), -1)
    return scores


def populate_table(table, scores, log_name, metric, model_type):
    row = log_names.index(log_name)
    column = metrics.index(metric) * len(model_types) * 2 + model_types.index(model_type) * len(model_types)

    table[row, column] = scores[0]
    if scores.shape[0] == 2:
        table[row, column + 1] = scores[1]


def print_latex_table(populated_table):
    print('\\begin{tabular}{|l||cccc||cccc||cccc|}')
    print('\\hline')
    print('& '),
    for i, metric in enumerate(metrics):
        print('\\multicolumn{4}{|c|}{\\textbf{' + metric + '}}'),
        if i != len(metrics) - 1:
            print(' & '),
        else:
            print('\\\\')
    print('\\hline\\hline')
    for i, log_name in enumerate(log_names):
        print(log_name.replace('_', '\_') + ' & '),
        for j, score in enumerate(populated_table[i]):
            print('%.2f' % score),
            if j != populated_table.shape[1] - 1:
                print(' & '),
            else:
                print('\\\\')
    print('\\hline')
    print('\\end{tabular}')


def show_comparison_image(populated_table, reference_table):
    reference_table[populated_table == 0] = 0

    plt.figure()
    plt.imshow((populated_table - reference_table)[:, [0, 2, 3, 4, 6, 7, 10, 11]])
    plt.yticks(range(len(log_names)), log_names)
    plt.xticks(range(len(headers)), headers, rotation=90)
    plt.colorbar()
    plt.tight_layout()
    plt.show()


def main():
    populated_table = np.zeros((len(log_names), len(metrics) * len(model_types) * 2))

    base_folderpath = 'output_files/final_experiments/results/'

    for log_name in log_names:
        for metric in metrics:
            for model_type in model_types:
                if metric == 'declare' and model_type == 'CF':
                    continue
                filepath = base_folderpath + metric + '/' + log_name + '_' + model_type + '.csv'
                try:
                    scores = parse_log(filepath, model_type == 'CFR')
                    populate_table(populated_table, scores, log_name, metric, model_type)
                except:
                    pass

    show_comparison_image(populated_table, reference_table)
    print_latex_table(populated_table)


if __name__ == "__main__":
    main()
