import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Gravity"

G = 50000

EARTH_VELOCITY = (0, 0)
MARS_VELOCITY = (0, 0)
WENUS_VELOCITY = (0, 0)
EARTH_MASS = 35
WENUS_MASS  = 50
MARS_MASS = 50


window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, False)
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, 0

Earth = pymunk.Body(EARTH_MASS, 5000)
Earth.position = 0.5*SCREEN_WIDTH, 0.*SCREEN_HEIGHT
Earth_shape = pymunk.Circle(Earth, 15)
Earth._set_velocity(EARTH_VELOCITY)

Mars = pymunk.Body(MARS_MASS, 50000)
Mars.position = 0.4*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT
Mars_shape = pymunk.Circle(Mars, 20)
Mars._set_velocity(MARS_VELOCITY)

Wenus = pymunk.Body(WENUS_MASS, 50000)
Wenus.position = 0.5*SCREEN_WIDTH, 0.75*SCREEN_HEIGHT
Wenus_shape = pymunk.Circle(Wenus, 25)
Wenus._set_velocity(WENUS_VELOCITY)




space.add(Earth, Earth_shape, Mars, Mars_shape, Wenus, Wenus_shape)

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)

def Force(obj1, obj2):
    r = obj1.position - obj2.position
    output = -r * G * obj1.mass * obj2.mass / r.get_length() ** 3
    return output

def update(dt):
    space.step(dt)
    fmars_earth = Force(Mars, Earth)
    fwenus_earth = Force(Wenus, Earth)
    fmars_wenus = Force(Mars, Wenus)
    Earth._set_force(-fmars_earth - fwenus_earth)
    Mars._set_force(fmars_earth + fmars_wenus)
    Wenus._set_force(fwenus_earth - fmars_wenus)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
