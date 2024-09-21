import os
import gradio as gr
from PIL import Image
import re


def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

folder1 = "" # Path to first image folder
folder2 = "" # Path to second image folder
logfile = "log.txt"
folder1_label = "" # Label under the images from first image folder
folder2_label = "" # Label under the images from first image folder
images1 = sorted([f for f in os.listdir(folder1) if f.endswith(('.png', '.jpg', '.jpeg'))], key=extract_number)
images2 = sorted([f for f in os.listdir(folder2) if f.endswith(('.png', '.jpg', '.jpeg'))], key=extract_number)
start_index = 0

def get_image_pairs():
    paired_images = [os.path.join(folder1, images1[start_index]), os.path.join(folder2, images2[start_index])]
    
    return paired_images

def update_images():
    global start_index
    paired_images = get_image_pairs()
    start_index += 1
    if start_index < len(images1):
        img1_path, img2_path = paired_images[0], paired_images[1]
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        current = f"{start_index + 2}/{len(images1)}"
        return img1, img2, current
    else:
        return None, None, "No more images"

def log_image():
    if start_index < len(images1):
        img1_path = images1[start_index - 1]
        image_name = os.path.basename(img1_path)
        
        with open(logfile, "a") as f:
            f.write(image_name + "\n")
    
    return update_images()

def skip_image():
    return update_images()


with gr.Blocks(analytics_enabled=False) as demo:

    with gr.Row():
        img1_output = gr.Image(label=folder1_label)
        img2_output = gr.Image(label=folder2_label)
    
    current_image_text = gr.Textbox(label="Image Pair Progress", interactive=False)
    
    with gr.Row():
        skip_button = gr.Button("Skip")
        log_button = gr.Button("Log and Next")

    skip_button.click(skip_image, inputs=[], outputs=[img1_output, img2_output, current_image_text])
    log_button.click(log_image, inputs=[], outputs=[img1_output, img2_output, current_image_text])

demo.launch(share=False)
