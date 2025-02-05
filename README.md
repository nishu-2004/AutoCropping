# ROI Bounding Box Visualization for Azure Kinect Camera

## Overview
This script is designed to visualize the Region of Interest (ROI) bounding boxes for both the RGB and infrared (IR) images captured by the Azure Kinect camera. It utilizes a predefined vector table containing ROI parameters corresponding to different distances to ensure precise alignment and validation of the ROIs for image processing tasks.

## Vector Table Structure
The vector table should be structured as follows:

| Distance | X_RGB | Y_RGB | Width_RGB | Height_RGB | X_IR | Y_IR | Width_IR | Height_IR |
|----------|-------|-------|-----------|------------|------|------|----------|-----------|

Where:
- **Distance**: The distance at which the ROI parameters were measured.
- **X_RGB, Y_RGB**: The top-left coordinates of the RGB image ROI.
- **Width_RGB, Height_RGB**: The width and height of the RGB image ROI.
- **X_IR, Y_IR**: The top-left coordinates of the IR image ROI.
- **Width_IR, Height_IR**: The width and height of the IR image ROI.

## Functionality
The script performs the following tasks:
- Captures **four consecutive frames** from the Azure Kinect camera.
- Reads the vector table containing ROI parameters.
- Extracts the ROI from the entire Azure Kinect camera image using the coordinates from the vector table.
- Crops the **driver's face** based on the extracted ROI.
- Overlays the bounding boxes on both the RGB and IR images.
- Displays the images using `imshow()` for visualization of the cropping regions before extracting the ROI.

This ensures accurate visualization and validation of the ROI bounding boxes before proceeding with further image processing.

## Benefits
- **Improved Object Detection**: Helps mitigate issues faced by YOLOv8 models, such as false detections of passengers instead of the driver.
- **Optimized Image Processing**: The reduction in image size enhances detection speed and processing efficiency.
- **Alignment Accuracy**: Ensures correct ROI extraction, leading to better performance in downstream tasks.
- **Avoids Overloading the Model**: The pre-trained model was not used as it could result in overloading the model.
- **Better Performance in Low-Light Conditions**: Pre-trained models do not normally work well in bad lighting conditions, making this customized approach more reliable.

This implementation is essential for optimizing object detection models and ensuring accurate region extraction in computer vision applications using the Azure Kinect camera.

