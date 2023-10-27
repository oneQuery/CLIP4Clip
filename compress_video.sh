#!/bin/bash

RAW_VIDEOS_DIR='/data/pia-data/msrvtt/MSRVTT/videos/all'
COMPRESSED_VIDEOS_DIR='/data/pia-data/msrvtt/msrvtt_data/MSRVTT_Videos'

# check if video source directory is correct
if [ ! -d "$RAW_VIDEOS_DIR" ]; then
    echo "Directory $RAW_VIDEOS_DIR does not exist. Please download the videos and place them in the directory."
    exit 1
fi

python preprocess/compress_video.py --input_root $RAW_VIDEOS_DIR --output_root $COMPRESSED_VIDEOS_DIR