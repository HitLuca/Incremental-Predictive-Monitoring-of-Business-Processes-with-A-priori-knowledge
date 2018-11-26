# Incremental_predictive_monitoring_of_Business_Processes_with_a_priori_knowledge

## Description
Continuation of [this](https://github.com/kaurjvpld/Incremental-Predictive-Monitoring-of-Business-Processes-with-A-priori-knowledge) project in which a predictive model is tasked to predict the continuation of a business process.

The input consists of categorical variables as well as real-valued timestamps, and the prediction consists of next time-step variables.

In this project, we leverage given Multi-Perspective A-priori Knowledge to improve inference on new data.

This repo is based on code from:

* [Process-Sequence-Prediction-with-A-priori-knowledge](https://github.com/yesanton/Process-Sequence-Prediction-with-A-priori-knowledge)
* [ProcessSequencePrediction](https://github.com/verenich/ProcessSequencePrediction)

The LTLCheckForTraces.jar program is an artifact generated from the code at [this](https://github.com/HitLuca/LTLCheckForTraces) repo.

### Predictive model
This contribution aims at improving the existing predictive model only, without improving/developing the existing prediction methods

### Inference algorithms
The project is divided into Control Flow (CF) prediction and Control Flow + Resource (CFR) prediction. At the moment, control flow and resource consist of categorical variables

#### Control Flow inference algorithms
* _6_evaluate_baseline_SUFFIX_only -> Baseline 1 - no a-priori knowledge is used and only the control-flow is predicted.
* _11_cycl_pro_SUFFIX_only -> This is Baseline 2 - a-priori knowledge is used on the control-flow and only the control-flow is predicted.

#### Control Flow + Resource inference algorithms
* _6_evaluate_baseline_SUFFIX_and_group -> Extended version of Baseline 1, where also the resource attribute is predicted.
* _11_cycl_pro_SUFFIX_resource_LTL -> Extended version of Baseline 2, where a-priori knowledge is used on the control-flow but also the resource attribute is predicted.
* _11_cycl_pro_SUFFIX_declare_smart_queue -> Proposed approach, where a-priori knowledge is used on the control-flow and on the resource attribute. Both the control-flow and the resource are predicted.

## Getting started
This project is intended to be self-contained, so no extra files are required

### Prerequisites
Necessary libraries are indicated in the requirements.txt, to install them run

```pip install -r requirements.txt````

### How to run the algorithms:

It is necessary to first start the Java server found in LTLCheckForTraces/StackEntryPoint.java. The server contains the code for checking the compliance with a single trace and the specified apriori knowledge. The proposed approach uses the DeclareAnalyzer plugin implemented for Prom. 

Every csv file should be converted into the suitable format(only numerical values) using the files src/support_scripts/csv_converter.py and src/support_scripts/csv_converter_group.py accordingly. The scripts also create dictionaries which map the numerical values to actual values.

Baseline 2 uses apriori knowledge in the form of LTL rules which are expressed in the src/shared_variables.py file. 

The proposed approach uses apriori knowledge in the form of MP-Declare rules, wchich are held in a separate file. The creation of the models can be done by following the structure found in the models in src/declare_models/.

The specification of the variables used for the experiments is done in the file src/shared_variables.py.

The file src/experiments_runner.py is used to run the the inference algorithms, which output the results to the folder output_files/.


