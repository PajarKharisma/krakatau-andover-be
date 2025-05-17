import cv2
import os
import time
import numpy as np
import logging
from config import context

def gen_surface_frames():  
    while context.VALUES['surface_camera_connect']:
        if isinstance(context.VALUES['surface_camera_frame'], np.ndarray):
            ret, buffer = cv2.imencode('.jpg', context.VALUES['surface_camera_frame'])
        else:
            logging.error("Surface camera frame is not a numpy array")
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_underwater_frames():
    while context.VALUES['underwater_camera_connect']:
        if isinstance(context.VALUES['underwater_camera_frame'], np.ndarray):
            ret, buffer = cv2.imencode('.jpg', context.VALUES['underwater_camera_frame'])
        else:
            logging.error("Underwater camera frame is not a numpy array")
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def capture_surface_camera():
    if os.path.exists("public/img/surface.png"):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        os.rename("public/img/surface.png", f"public/img/surface-{timestamp}.png")
    cv2.imwrite(f"public/img/surface.png", context.VALUES['surface_camera_frame'])

def capture_underwater_camera():
    if os.path.exists("public/img/underwater.png"):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        os.rename("public/img/underwater.png", f"public/img/underwater-{timestamp}.png")
    cv2.imwrite(f"public/img/underwater.png", context.VALUES['underwater_camera_frame'])

def get_latest_surface_image():
    if os.path.exists("public/img/surface.png"):
        return cv2.imread("public/img/surface.png")
    return None
    
def get_latest_underwater_image():
    if os.path.exists("public/img/underwater.png"):
        return cv2.imread("public/img/underwater.png")
    return None

