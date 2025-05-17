from flask import Response, make_response
from app import app
import cv2
from flask import Blueprint

from config import context
from services import cameraService
from utils import httpResponse

cameraBp = Blueprint('camera', __name__, url_prefix='/camera')


@cameraBp.route("/")
def get_image():
    retval, buffer = cv2.imencode('.png', context.VALUES['surface_camera_frame'])
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@cameraBp.route("/surface-capture")
def capture_surface():
    cameraService.capture_surface_camera()
    return httpResponse.success({"message": "success"})

@cameraBp.route("/underwater-capture")
def capture_underwater():
    cameraService.capture_underwater_camera()
    return httpResponse.success({"message": "success"})

@cameraBp.route("/surface-latest")
def get_latest_surface():
    image = cameraService.get_latest_surface_image()
    if image is None:
        return httpResponse.error({"message": "Image not found"})
    retval, buffer = cv2.imencode('.png', image)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@cameraBp.route('/underwater-latest')
def get_latest_underwater():
    image = cameraService.get_latest_underwater_image()
    if image is None:
        return httpResponse.error({"message": "Image not found"})
    retval, buffer = cv2.imencode('.png', image)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@cameraBp.route('/surface-stream')
def video_feed_surface():
    return Response(cameraService.gen_surface_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@cameraBp.route('/underwater-stream')
def video_feed_underwater():
    return Response(cameraService.gen_underwater_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')