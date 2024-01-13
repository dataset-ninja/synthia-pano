**SYNTHIA-PANO Panoramic Image Dataset** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the automotive industry. 

The dataset consists of 3236 images with 785441 labeled objects belonging to 14 different classes including *building*, *car*, *landmarking*, and other: *pole*, *road*, *sky*, *vegetation*, *void*, *traffic sign*, *sidewalk*, *pedestrian*, *traffic light*, *fence*, and *bicycle*.

Images in the SYNTHIA-PANO dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. Additionally, each image contains information about its ***subfolder***. Explore it in supervisely supervisely labeling tool. The dataset was released in 2019 by the College of Optical Science and Engineering, Zhejiang University, China.

Here are the visualized examples for the classes:

[Dataset classes](https://github.com/dataset-ninja/synthia-pano/raw/main/visualizations/classes_preview.webm)
