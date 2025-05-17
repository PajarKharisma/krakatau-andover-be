from config import context
from datetime import datetime

def setContext(payload):
    for key, value in payload.items():
        context.VALUES[key] = value

def getContext():
    response = {
        'app_connect': context.VALUES['app_connect'],
        'pitch': context.VALUES['pitch'],
        'roll': context.VALUES['roll'],
        'yaw': context.VALUES['yaw'],
        'lat': context.VALUES['lat'],
        'long': context.VALUES['long'],
        'alt': context.VALUES['alt'],
        'battery': context.VALUES['battery'],
        'is_armable': context.VALUES['is_armable'],
        'system_status': context.VALUES['system_status'],
        'mode': context.VALUES['mode'],
        'last_heartbeat': context.VALUES['last_heartbeat'],
        'surface_camera_connect': context.VALUES['surface_camera_connect'],
        'underwater_camera_connect': context.VALUES['underwater_camera_connect'],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S'),
        'depth': context.VALUES['depth']
    }
    return response
