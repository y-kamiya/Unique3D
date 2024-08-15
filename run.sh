#!/bin/bash -eu

source $1/bin/activate
python app/gradio_local.py --port 7860 --listen
#python app/custom_models/mvimg_prediction.py "<image path>"
