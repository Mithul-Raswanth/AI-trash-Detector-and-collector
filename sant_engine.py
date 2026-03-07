import cv2
import numpy as np
# We import Mith's file here so we can use his logic
from mith_ai import apply_ai_vision
def get_processed_stream(ip_address):
# Note: If the IP has 'http://' remove it, we format it cleanly here
    clean_ip = ip_address.replace("http://", "").replace("/", "")
    stream_url = f"http://{clean_ip}:81/stream"
    # Open the video link
    cap = cv2.VideoCapture(stream_url)
    # Read one frame
    ret, frame = cap.read()
    # Close the connection immediately to save bandwidth
    cap.release()
    if ret:
    # If we got a picture, send it to Mith
        ai_frame = apply_ai_vision(frame)
        return ai_frame
    else:
# If connection failed, return Nothing
        return None