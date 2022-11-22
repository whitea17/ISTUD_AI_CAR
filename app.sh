#!/bin/bash
# Script called through docker cmd in standard operation
echo $MODEL
echo $MODEL_LABELS
echo $OUTPUT_STREAM

python3 ./AI_detection.py --model=$MODEL --labels=$MODEL_LABELS $OUTPUT_STREAM
