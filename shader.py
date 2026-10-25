# creates a sun and simple shaders

import colors
from panda3d.core import DirectionalLight, AmbientLight, Vec4

class Shader:
    def __init__(self, app):
        self.app = app

        sun = DirectionalLight("sun")
        sun.setColor(colors.SUN)
        sun.setShadowCaster(True, 2048, 2048)

        sun_path = app.render.attachNewNode(sun)
        sun_path.setHpr(-45, -60, 0)
        app.render.setLight(sun_path)

        ambient = AmbientLight("ambient")
        ambient.setColor(colors.AMBIENT)

        ambient_path = app.render.attachNewNode(ambient)
        app.render.setLight(ambient_path)

        app.render.setShaderAuto()
