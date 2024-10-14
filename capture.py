
import subprocess
import cv2
import numpy as np
import os

def capture_monitor(monitor_name):
    # Define the command to run wf-recorder and pipe the output to GStreamer
    wf_recorder_cmd = [
        "wf-recorder",
        "-o", monitor_name,
        "-f", "/dev/stdout",
        "-t", "raw"
    ]

    # Define the GStreamer pipeline to read from stdin and convert the video format
    gst_pipeline = (
        "fdsrc ! "
        "rawvideoparse format=rgba width=1920 height=1080 framerate=30/1 ! "
        "videoconvert ! "
        "video/x-raw,format=BGR ! "
        "appsink"
    )

    # Open the video capture with the GStreamer pipeline
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    # Start the wf-recorder process
    wf_recorder_process = subprocess.Popen(wf_recorder_cmd, stdout=subprocess.PIPE)

    if not cap.isOpened():
        print("Error: Could not open video capture")
        wf_recorder_process.terminate()
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        # Display the frame using OpenCV
        cv2.imshow("Monitor Capture", frame)

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    wf_recorder_process.terminate()

# Example usage
monitor_name = "HDMI-A-1"  # Replace with the correct monitor identifier (e.g., HDMI-A-1, DP-1)
capture_monitor(monitor_name)
