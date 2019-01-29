# Incremental predictive monitoring of Business Processes with a-priori knowledge

## Description
Continuation of [this](https://github.com/kaurjvpld/Incremental-Predictive-Monitoring-of-Business-Processes-with-A-priori-knowledge) project in which a predictive model is tasked to predict the continuation of a business process.

The input consists of categorical variables, indicating an activity ID and a resource ID, as well as real-valued variables, indicating for example elapsed time. The prediction consists of next time-step variables.

In this project, we leverage given Multi-Perspective A-priori Knowledge to improve inference on new data.

This repo is based on code from:

* [Process-Sequence-Prediction-with-A-priori-knowledge](https://github.com/yesanton/Process-Sequence-Prediction-with-A-priori-knowledge)
* [ProcessSequencePrediction](https://github.com/verenich/ProcessSequencePrediction)

The LTLCheckForTraces.jar program is an artifact generated from the code at [this](https://github.com/HitLuca/LTLCheckForTraces) repo.

### Predictive model
This contribution aims at improving the existing predictive model only, without improving/developing the existing inference algorithms used for evaluation.

### Inference algorithms
The project is divided into Control Flow (CF) prediction and Control Flow + Resource (CFR) prediction. At the moment, control flow and resource consist of categorical variables.
Time has also been added as a prediction element, creating the Control Flow + Resource + Time (CFRT) acronym.

#### Control Flow inference algorithms
* [baseline_1_cf](src/evaluation/inference_algorithms/baseline_1_cf.py) -> Baseline 1 - no a-priori knowledge is used and only the control-flow is predicted.
* [baseline_2_cf](src/evaluation/inference_algorithms/baseline_2_cf.py) -> This is Baseline 2 - a-priori knowledge is used on the control-flow and only the control-flow is predicted.

#### Control Flow + Resource inference algorithms
* [baseline_1_cfr](src/evaluation/inference_algorithms/baseline_1_cfr.py) -> Extended version of Baseline 1, where also the resource attribute is predicted.
* [baseline_2_cfr](src/evaluation/inference_algorithms/baseline_2_cfr.py) -> Extended version of Baseline 2, where a-priori knowledge is used on the control-flow but also the resource attribute is predicted.
* [new_method_cfr](src/evaluation/inference_algorithms/new_method_cfr.py) -> Proposed approach, where a-priori knowledge is used on the control-flow and on the resource attribute. Both the control-flow and the resource are predicted.

## Project structure

The [src](src) folder contains all the scripts used.

[experiment_runner](src/experiments_runner.py) is used to train and evaluate the predictive models.

The [inference_algorithms](src/evaluation/inference_algorithms) folder contains all the inference algorithms available.

Results are saved into the [output_files](output_files) folder.

[shared_variables.py](src/shared_variables.py) contains meta-variables used at inference-time, as well as training/model hyperparameters.

[parse_results.py](src/parse_results.py) parses the results contained in the [results]() folder inside each model run, and plots multiple images/tables that allow quick comparisons.

## Getting started
This project is intended to be self-contained, so no extra files are required.

### Prerequisites
To install the python environment for this project, refer to the [Pipenv setup guide](https://pipenv.readthedocs.io/en/latest/basics/)

### Running the algorithms
As the Java server is now integrated in the project, there is no need to start it separately.

The [experiment_runner.py](src/experiments_runner.py) file contains all the code necessary to train the predictive models on each log file and evaluate them with each inference method.

The [run_experiments](src/run_experiments.sh) script allows the user to train both old and new implementations of the predictive model on all the datasets automatically.

#### Training the predictive models
Simply run the [experiment_runner.py](src/experiments_runner.py) script with the --train flag. If no option is specified the script will train and test automatically the model

#### Evaluating the predictive models
Simply run the [experiment_runner.py](src/experiments_runner.py) script with the --evaluate flag. If no option is specified the script will train and test automatically the model

#### Elaborating the results
In order to check improvements between this project and its original implementation, run the  [parse_results.py](src/parse_results.py) script, indicating the folder for the two models before running it.
