import cv2
import numpy as np
import pandas as pd
import os
import pykinect_azure as pykinect

def capture_frames_from_camera(num_frames=4, rotate_flag=True):
    # Initialize the Azure Kinect SDK
    pykinect.initialize_libraries()

    # Configure the device settings
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED  # 2x2 binned mode for depth/IR
    device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30

    # Start the device
    device = pykinect.start_device(config=device_config)
    frames = []
    for _ in range(num_frames):
        capture = device.update()

        # Capture RGB and IR images
        ret_rgb, rgb_image = capture.get_color_image()
        ret_ir, ir_image = capture.get_ir_image()

        if not ret_rgb or not ret_ir:
            print("Failed to capture a frame.")
            continue

        # Process IR Image
        ir_image = cv2.convertScaleAbs(ir_image, alpha=0.2, beta=0.009)

        # Resize IR to match the desired output size
        ir_image = cv2.resize(ir_image, (512, 512))

        # Process RGB Image
        rgb_image = cv2.convertScaleAbs(rgb_image, alpha=1.0, beta=0.0)

        # Resize RGB to match the desired output resolution
        rgb_image = cv2.resize(rgb_image, (1520, 720))

        if rotate_flag:
            rgb_image = cv2.rotate(rgb_image, cv2.ROTATE_180)
            ir_image = cv2.rotate(ir_image, cv2.ROTATE_180)

        frames.append((rgb_image, ir_image))
        print("Captured and processed a frame.")

    return frames

def draw_bounding_boxes(image, boxes, color=(0, 255, 0)):
    for box in boxes:
        x, y, w, h = box
        top_left = (max(0, int(x - w/2)), max(0, int(y - h/2)))
        bottom_right = (min(image.shape[1], int(x + w/2)), min(image.shape[0], int(y + h/2)))
        cv2.rectangle(image, top_left, bottom_right, color, 2)
    return image

def display_frames_with_bounding_boxes(frames, rgb_box, ir_box):
    for rgb_image, ir_image in frames:
        # Draw bounding boxes
        rgb_with_boxes = draw_bounding_boxes(rgb_image.copy(), [rgb_box])
        ir_with_boxes = draw_bounding_boxes(ir_image.copy(), [ir_box], color=(255, 0, 0))

        # Show frames
        cv2.imshow("RGB with Bounding Box", rgb_with_boxes)
        cv2.imshow("IR with Bounding Box", ir_with_boxes)

        key = cv2.waitKey(0)  # Wait for a key press to proceed to the next frame
        if key == ord('q'):  # Exit on 'q' key press
            break

    cv2.destroyAllWindows()

def main():
    vector_table_path = input("Enter the full path to the vector table (CSV file): ")
    if not os.path.exists(vector_table_path):
        print(f"Error: Vector table file '{vector_table_path}' not found.")
        return

    try:
        target_distance = float(input("Enter the target distance for bounding box: "))
    except ValueError:
        print("Invalid distance entered. Please enter a numeric value.")
        return

    print("Capturing frames...")
    frames = capture_frames_from_camera()

    print("Reading vector table...")
    df = pd.read_csv(vector_table_path)

    rgb_columns = ['Avg_X_RGB', 'Avg_Y_RGB', 'Avg_Width_RGB', 'Avg_Height_RGB']
    ir_columns = ['Avg_X_IR', 'Avg_Y_IR', 'Avg_Width_IR', 'Avg_Height_IR']

    # Get bounding boxes
    if target_distance in df['Distance'].values:
        rgb_box = df[df['Distance'] == target_distance][rgb_columns].values[0]
        ir_box = df[df['Distance'] == target_distance][ir_columns].values[0]
    else:
        print("Target distance not found in vector table.")
        return

    print("Displaying frames with bounding boxes...")
    display_frames_with_bounding_boxes(frames, rgb_box, ir_box)

if __name__ == "__main__":
    main()