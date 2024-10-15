
import os
import subprocess
import json
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import time

# Set environment variable to use XCB plugin
os.environ['QT_QPA_PLATFORM'] = 'xcb'

def get_window_geometry(window_name):
    try:
        # Use hyprctl to get window information
        hyprctl_command = ['hyprctl', 'clients', '-j']
        result = subprocess.run(hyprctl_command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"hyprctl command failed: {result.stderr}")
            return None
        
        windows = json.loads(result.stdout)
        for window in windows:
            if window_name in window['title']:
                x = window['at'][0]
                y = window['at'][1]
                width = window['size'][0]
                height = window['size'][1]
                geometry = f"{x},{y} {width}x{height}"
                return geometry
        
        print(f"Window with name '{window_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching window geometry: {e}")
        return None

def capture_frame(geometry):
    try:
        # Use grim to capture the selected window
        grim_command = ['grim', '-g', geometry, '-']
        grim_output = subprocess.run(grim_command, capture_output=True)
        
        if grim_output.returncode != 0:
            print(f"Grim capture failed: {grim_output.stderr}")
            return None
        
        # Read the image from grim's output
        image = Image.open(BytesIO(grim_output.stdout))
        img_np = np.array(image)
        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        return frame
    except Exception as e:
        print(f"An error occurred during frame capture: {e}")
        return None

def main(window_name):
    # Get geometry of the window to capture
    geometry = get_window_geometry(window_name)
    if not geometry:
        return
    
    while True:
        # Capture the frame
        frame = capture_frame(geometry)
        if frame is None:
            break

        # Example analysis: Convert to grayscale and detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        # Display the original frame and the edge-detected frame
        cv2.imshow('Captured Frame', frame)
        #cv2.imshow('Edges', edges)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Sleep for a short duration to control the frame rate
        time.sleep(0.1)  # Adjust the sleep duration as needed

    cv2.destroyAllWindows()

if __name__ == "__main__":
    window_name = "DRL Simulator"  # Replace with the actual window name
    main(window_name)
