from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import atexit
import signal
import logging
from config import context
from jobs.serialJob import SerialThread
from jobs.surfaceCameraJob import SurfaceCameraThread
from jobs.underwaterCameraJob import UnderwaterCameraThread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
app.secret_key = os.urandom(24)

from views import *

logging.basicConfig(level=logging.INFO)

# Global variable to track the thread instance
serial_thread = None
surface_camera_thread = None
underwater_camera_thread = None

def start_serial_thread():
    global serial_thread
    if serial_thread is None or not serial_thread.is_alive():
        logging.info("Starting serial thread...")
        serial_thread = SerialThread('serial_thread')
        serial_thread.daemon = True
        serial_thread.start()
    else:
        logging.info("Serial thread already running.")

start_serial_thread()

def start_surface_camera_thread():
    global surface_camera_thread
    if surface_camera_thread is None or not surface_camera_thread.is_alive():
        logging.info("Starting surface camera thread...")
        surface_camera_thread = SurfaceCameraThread('surface_camera_thread')
        surface_camera_thread.daemon = True
        surface_camera_thread.start()
    else:
        logging.info("Surface camera thread already running.")

start_surface_camera_thread()

def start_underwater_camera_thread():
    global underwater_camera_thread
    if underwater_camera_thread is None or not underwater_camera_thread.is_alive():
        logging.info("Starting underwater camera thread...")
        underwater_camera_thread = UnderwaterCameraThread('underwater_camera_thread')
        underwater_camera_thread.daemon = True
        underwater_camera_thread.start()
    else:
        logging.info("Underwater camera thread already running.")

start_underwater_camera_thread()

def cleanup():
    logging.info("Stopping background thread...")
    if serial_thread is not None:
        serial_thread.stop()
        serial_thread.join()
    if surface_camera_thread is not None:
        surface_camera_thread.stop()
        surface_camera_thread.join()
    if underwater_camera_thread is not None:
        underwater_camera_thread.stop()
        underwater_camera_thread.join()
    logging.info("Background thread stopped.")

atexit.register(cleanup)

def handle_signal(signal, frame):
    cleanup()
    os._exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
    context.VALUES['app_connect'] = False
    context.VALUES['surface_camera_connect'] = False
    context.VALUES['underwater_camera_connect'] = False
