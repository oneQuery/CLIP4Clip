#!/bin/bash

# For SAFETY data
python main_format_conversion.py \
--input_jsons_dir /data/pia-data/alchera/annotations/safety_json \
--output_dir output_alchera2msrvtt \
--output_json_filename alchera2msrvtt_safety.json \
--source_format alchera \
--target_format msrvtt \

# For TOUR data
python main_format_conversion.py \
--input_jsons_dir /data/pia-data/alchera/annotations/tour_json \
--output_dir output_alchera2msrvtt \
--output_json_filename alchera2msrvtt_tour.json \
--source_format alchera \
--target_format msrvtt \