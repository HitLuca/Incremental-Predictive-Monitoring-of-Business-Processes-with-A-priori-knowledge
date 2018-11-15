import csv

import numpy as np
from tabulate import tabulate

log_names = ['10x2_1W', '10x2_3W', '10x2_1S', '10x2_3S', '10x5_1W', '10x5_3W', '10x5_1S', '10x5_3S', '10x20_1W',
             '10x20_3W', '10x20_1S', '10x20_3S', '5x5_1W', '5x5_3W', '5x5_1S', '5x5_3S', '50x5_1W', '50x5_3W',
             '50x5_1S', '50x5_3S']  # , 'BPI2017_50k']

metrics = ['baseline', 'LTL', 'declare']

model_types = ['CF', 'CFR']


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
            if score_1 > 1:
                score_1 /= 1000.0
            scores[0].append(score_1)

            if two_predictions:
                score_2 = float(row[headers.index(label_2)])
                if score_2 > 1:
                    score_2 /= 1000.0
                scores[1].append(score_2)

    scores = np.mean(np.array(scores), -1)
    return scores


def populate_table(table, scores, log_name, metric, model_type):
    row = log_names.index(log_name)
    column = metrics.index(metric) * len(model_types) * 2 + model_types.index(model_type) * len(model_types)

    table[row, column] = scores[0]
    if scores.shape[0] == 2:
        table[row, column+1] = scores[1]


def main():
    table = np.zeros((len(log_names), len(metrics) * len(model_types) * 2))
    base_folderpath = 'output_files/final_experiments/results/'

    for log_name in log_names:
        for metric in metrics:
            for model_type in model_types:
                if metric == 'declare' and model_type == 'CF':
                    continue
                filepath = base_folderpath + metric + '/' + log_name + '_' + model_type + '.csv'
                try:
                    scores = parse_log(filepath, model_type == 'CFR')
                    populate_table(table, scores, log_name, metric, model_type)
                except:
                    pass

    print(tabulate(table, tablefmt='latex', floatfmt='.2f'))


if __name__ == "__main__":
    main()
