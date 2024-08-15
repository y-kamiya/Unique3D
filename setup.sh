#!/bin/bash -x

venv=$1
if [ ! -d $venv ]; then
    python -m venv $venv
fi
source $venv/bin/activate

pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
pip install ninja diffusers==0.27.2
pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.3.1/index.html
pip install -r requirements.txt
pip install -e .
