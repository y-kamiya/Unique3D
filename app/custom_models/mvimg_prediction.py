import sys
import torch
import gradio as gr
from PIL import Image
import numpy as np
from rembg import remove
from app.utils import change_rgba_bg, rgba_to_rgb
from app.custom_models.utils import load_pipeline
from scripts.all_typing import *
from scripts.utils import session, simple_preprocess

training_config = "app/custom_models/image2mvimage.yaml"
checkpoint_path = "ckpt/img2mvimg/unet_state_dict.pth"
trainer, pipeline = load_pipeline(training_config, checkpoint_path)
# pipeline.enable_model_cpu_offload()

def predict(img_list: List[Image.Image], guidance_scale=2., **kwargs):
    if isinstance(img_list, Image.Image):
        img_list = [img_list]
    img_list = [rgba_to_rgb(i) if i.mode == 'RGBA' else i for i in img_list]
    ret = []
    for img in img_list:
        images = trainer.pipeline_forward(
            pipeline=pipeline,
            image=img,
            guidance_scale=guidance_scale, 
            **kwargs
        ).images
        ret.extend(images)
    return ret


def run_mvprediction(input_image: Image.Image, remove_bg=True, guidance_scale=1.5, seed=1145):
    if input_image.mode == 'RGB' or np.array(input_image)[..., -1].mean() == 255.:
        # still do remove using rembg, since simple_preprocess requires RGBA image
        print("RGB image not RGBA! still remove bg!")
        remove_bg = True

    if remove_bg:
        input_image = remove(input_image, session=session)

    # make front_pil RGBA with white bg
    input_image = change_rgba_bg(input_image, "white")
    single_image = simple_preprocess(input_image)

    generator = torch.Generator(device="cuda").manual_seed(int(seed)) if seed >= 0 else None

    rgb_pils = predict(
        single_image,
        generator=generator,
        guidance_scale=guidance_scale,
        width=256,
        height=256,
        num_inference_steps=30,
    )

    return rgb_pils, single_image


import os
import argparse
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("input_path")
    parser.add_argument("--output_dir", type=Path, default="./output")
    args = parser.parse_args()
    print(args)

    os.makedirs(args.output_dir, exist_ok=True)

    img_pil = Image.open(args.input_path)
    rgb_pils, front_pil = run_mvprediction(img_pil, remove_bg=True, seed=1145)

    front_pil.save(args.output_dir / "front.png")
    for i, img in enumerate(rgb_pils):
        img.save(args.output_dir / f"{i}.png")
