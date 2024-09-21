import os
import gradio as gr
from PIL import Image
import re
import time


def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

folder1 = "" # Path to first image folder
folder2 = "" # Path to second image folder
logfile = "log.txt"

images1 = sorted([f for f in os.listdir(folder1) if f.endswith(('.png', '.jpg', '.jpeg'))], key=extract_number)
images2 = sorted([f for f in os.listdir(folder2) if f.endswith(('.png', '.jpg', '.jpeg'))], key=extract_number)
start_index = 0
showing_first_image = True  # Flag to track which image is shown (true for first image, false for second)

def get_image_pair():
    
    return os.path.join(folder1, images1[start_index]), os.path.join(folder2, images2[start_index])

def get_current_image():
    img1_path, img2_path = get_image_pair()

    if showing_first_image:
        img = Image.open(img1_path).convert("RGBA")
    else:
        img = Image.open(img2_path).convert("RGBA")

    return img

def update_image():
    global start_index
    if start_index < len(images1):
        current_img = get_current_image()
        current = f"{start_index + 1}/{len(images1)}"
        return current_img, current
    else:
        return None, "No more images"

def log_image_and_next():
    global start_index
    if start_index < len(images1):
        img1_path, _ = get_image_pair()
        image_name = os.path.basename(img1_path)
        
        with open(logfile, "a") as f:
            f.write(image_name + "\n")

    start_index += 1
    return update_image()

def skip_image():
    global start_index
    start_index += 1
    return update_image()

def toggle_image():
    global showing_first_image
    showing_first_image = not showing_first_image  # Toggle flag for other image
    return update_image()

shortcut_js = """
<script>
function shortcuts(e) {

    if (e.keyCode === 37 || e.keyCode === 81) {
        document.getElementById("skip").click();
    }
    else if (e.keyCode === 39 || e.keyCode === 80) {
        document.getElementById("log").click();
    }
    else if (e.keyCode === 32) {
        document.getElementById("toggle").click();
    }
}
document.addEventListener('keyup', shortcuts, false);
</script>
"""

with gr.Blocks(analytics_enabled=False, head=shortcut_js) as demo:

    img_output = gr.Image(label="Current Image", height=200)
    current_image_text = gr.Textbox(label="Image Pair Progress", interactive=False)

    def auto_toggle():
        while True:
            time.sleep(0.5)
            yield toggle_image()

    with gr.Row():
        skip_button = gr.Button("Skip", elem_id="skip")
        log_button = gr.Button("Log and Next", elem_id="log")
    # with gr.Row():
    #     toggle_button = gr.Button("Toggle Image", elem_id="toggle")
    
    skip_button.click(skip_image, inputs=[], outputs=[img_output, current_image_text], show_progress=False)
    log_button.click(log_image_and_next, inputs=[], outputs=[img_output, current_image_text], show_progress=False)
    # toggle_button.click(toggle_image, inputs=[], outputs=[img_output, current_image_text], show_progress=False)

    demo.load(auto_toggle, outputs=[img_output, current_image_text])
    

demo.launch(share=False)
