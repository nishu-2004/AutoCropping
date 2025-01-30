Here’s the updated technical description incorporating the multi-frame capture and display functionality:  

---

 **ROI Bounding Box Visualization for Azure Kinect Camera**  

This code is designed to visualize the Region of Interest (ROI) bounding boxes for both the RGB and infrared (IR) images captured by the Azure Kinect camera. It utilizes a predefined vector table containing ROI parameters corresponding to different distances.  

 **Vector Table Structure**  
The vector table should be structured with the following columns:  

| Distance | X_RGB | Y_RGB | Width_RGB | Height_RGB | X_IR | Y_IR | Width_IR | Height_IR |  
|----------|-------|-------|-----------|------------|------|------|----------|-----------|  

Where:  
- **Distance**: The distance at which the ROI parameters were measured.  
- **X_RGB, Y_RGB**: The top-left coordinates of the RGB image ROI.  
- **Width_RGB, Height_RGB**: The width and height of the RGB image ROI.  
- **X_IR, Y_IR**: The top-left coordinates of the IR image ROI.  
- **Width_IR, Height_IR**: The width and height of the IR image ROI.  

 **Functionality**  
The script:  
- Captures **four consecutive frames** from the Azure Kinect camera.  
- Reads the vector table containing ROI parameters.  
- Overlays the bounding boxes on both the RGB and IR images.  
- Displays the images using `imshow()` for visualization of the cropping regions before extracting the ROI.  

This ensures precise alignment and validation of the ROIs for image processing tasks.
