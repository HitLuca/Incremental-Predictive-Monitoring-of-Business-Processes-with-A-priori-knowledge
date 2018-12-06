#!/usr/bin/env bash
source ~/.bashrc

python_env

log_names=(
        "10x5_1S"
        "10x5_1W"
        "10x5_3S"
        "10x5_3W"
        "5x5_1W"
        "5x5_1S"
        "5x5_3W"
        "5x5_3S"
        "10x20_1W"
        "10x20_1S"
        "10x20_3W"
        "10x20_3S"
        "10x2_1W"
        "10x2_1S"
        "10x2_3W"
        "10x2_3S"
        "50x5_1W"
        "50x5_1S"
        "50x5_3W"
        "50x5_3S"
        )

for log_name in "${log_names[@]}"
do
    python experiments_runner.py ${log_name}
done

