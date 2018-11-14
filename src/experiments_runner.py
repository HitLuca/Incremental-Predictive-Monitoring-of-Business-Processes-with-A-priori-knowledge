"""
This file was created to manage running of experiments.

## settings are in the shared variables file
"""


from inference_algorithms import _6_evaluate_baseline_SUFFIX_only
from inference_algorithms import _6_evaluate_baseline_SUFFIX_and_group

from inference_algorithms import _11_cycl_pro_SUFFIX_only
from inference_algorithms import _11_cycl_pro_SUFFIX_resource_LTL

from inference_algorithms import _11_cycl_pro_SUFFIX_declare_smart_queue

import train, train_with_data

# formula_used = "WEAK"
# formula_used = "STRONG"
logNumber = 3

train.train(logNumber)
# train_with_data.train_with_data(logNumber)


# _6_evaluate_baseline_SUFFIX_only.run_experiments(logNumber, "STRONG", "CF")
# _6_evaluate_baseline_SUFFIX_and_group.run_experiments(logNumber, "STRONG", "CFR")

# _11_cycl_pro_SUFFIX_only.run_experiments(logNumber, "STRONG", "CF")
# _11_cycl_pro_SUFFIX_resource_LTL.run_experiments(logNumber, "STRONG", "CFR")

# _11_cycl_pro_SUFFIX_declare_smart_queue.run_experiments(logNumber, "STRONG", "CFR")
