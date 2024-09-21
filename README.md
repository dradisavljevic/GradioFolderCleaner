# GradioFolderCleaner

Simple Gradio application for comparing the images from two different folders in a head to head manner.

The images can either be compared shown one next to another by running the `gradio_head2head.py` file, or they can be shown changing within the same image field one over the other by running the `gradio_overlay.py`.

For easier comparions strategy, the program assumes that images will have names that are only numbers. If you wish to use the program for comparing images that include non-numeric characters, remove the `key=extract_number` argument from the sorting function at the start of the python files.

## Prerequisites

Before running the project, install the dependencies from requirements.txt file via pip using the

```
pip install -r requirements.txt
```

After that, add the path to two folders used for comparison (and optionally labels if you run `gradio_head2head.py`). Finally run the application with:

```
python gradio_{desired_comparison_mode}.py
```

The application should then run at http://127.0.0.1:7860.

## Application of the gradio results

Simple usage of the results produced by this gradio application can be removing unwanted images. Simple program for removing the unwanted image files (those that have been logged inside of the logfile) is implemented in the `flush.py` python file.