# Incremental predictive monitoring of Business Processes with a-priori knowledge

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
* ```_6_evaluate_baseline_SUFFIX_only``` -> Baseline 1 - no a-priori knowledge is used and only the control-flow is predicted.
* ```_11_cycl_pro_SUFFIX_only``` -> This is Baseline 2 - a-priori knowledge is used on the control-flow and only the control-flow is predicted.

#### Control Flow + Resource inference algorithms
* ```_6_evaluate_baseline_SUFFIX_and_group``` -> Extended version of Baseline 1, where also the resource attribute is predicted.
* ```_11_cycl_pro_SUFFIX_resource_LTL``` -> Extended version of Baseline 2, where a-priori knowledge is used on the control-flow but also the resource attribute is predicted.
* ```_11_cycl_pro_SUFFIX_declare_smart_queue``` -> Proposed approach, where a-priori knowledge is used on the control-flow and on the resource attribute. Both the control-flow and the resource are predicted.

## Project structure

The ```src``` folder contains all the scripts used.

```experiment_runner.py``` is used to train and evaluate the predictive models.

The ```inference_algorithms``` folder contains all the inference algorithms available, with the ones used located at ```inference_algorithms/used_algorithms```.

Results are saved into the ```output_files``` folder.

```shared_variables.py``` contains meta-variables used at inference-time.

```parse_results.py``` parses the results contained in ```output_files/final_experiments/results``` and plots multiple images/tables.

## Getting started
This project is intended to be self-contained, so no extra files are required.

### Prerequisites
To install the python environment for this project, refer to the [Pipenv setup guide](https://pipenv.readthedocs.io/en/latest/basics/)

### Running the algorithms
As the Java server is now integrated in the project, there is no need to start it separately.

The ```experiment_runner.py``` file contains all the code necessary to train the predictive models on each log file and evaluate them with each inference method.

#### Training the predictive models
make sure that both the ```train_cf.train(log_name)``` and ```train_cfr.train(log_name)``` lines are uncommented and run the ```experiments_runner.py``` script.

#### Evaluating the predictive models
make sure that the ```evaluate_all(log_name)``` line is uncommented and run the ```experiments_runner.py``` script.

#### Elaborating the results
In order to check improvements between this project and its original implementation, run the  ```parse_results.py``` script.

#### Speeding up the evaluation
As the evaluation part of the project tends to slow down substantially over time, I included a script that automatically runs a new instance of the ```experiments_runner.py``` script for each log file. To use this feature simply run the ```run_experiments.sh``` script with the log files you want to use selected.