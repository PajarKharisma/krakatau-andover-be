from app import app

from .homeView import homeBp
from .contextView import contextBp
from .cameraView import cameraBp

app.register_blueprint(homeBp)
app.register_blueprint(contextBp)
app.register_blueprint(cameraBp)