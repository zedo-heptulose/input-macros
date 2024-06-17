#!/bin/bash

cd "$(dirname "$0")"

# Loop through each subdirectory
for dir in */; do
    cd "$dir"
    for script in *.sh; do
        sbatch $script
    done
    cd ..
done
