#!/bin/bash

python main_format_merge.py \
--input_json_filepaths \
"output_alchera2msrvtt/alchera2msrvtt_safety.json" \
"output_alchera2msrvtt/alchera2msrvtt_tour.json" \
--output_dir "output_alchera2msrvtt_merged" \
--output_json_filename "alchera2msrvtt_merged.json" \
--format_type "msrvtt"