#!/bin/bash

conda install --yes -c pytorch pytorch=1.7.1 torchvision cudatoolkit=11.0
pip install ftfy regex tqdm
pip install opencv-python boto3 requests pandas

# install ffmpeg
sudo apt install ffmpeg
pip install ffmpeg