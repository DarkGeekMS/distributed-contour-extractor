#!/bin/bash
# This script initializes the whole pipeline
# It takes three inputs: host machine, video file path and number of intermediate nodes.

NODE_COUNT=$3
COLLECTOR_COUNT=$(python -c "from math import ceil; print(ceil($NODE_COUNT/2.0))")

if [ $1 -eq 1 ]; then

python back_machine/input_node.py -video_path $2

for i in $(seq 1 $NODE_COUNT)
do
    python back_machine/ostu_node.py
done

for i in $(seq 1 $COLLECTOR_COUNT)
do
    python back_machine/collector_node.py
done

elif [ $1 -eq 2 ]; then

for i in $(seq 1 $NODE_COUNT)
do
    python front_machine/contours_node.py
done

python front_machine/output_node.py

else

echo "Invalid machine number"

echo "Terminating ..."

fi