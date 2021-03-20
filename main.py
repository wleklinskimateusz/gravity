import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
from pyglet.window import key
from pyglet.window import mouse

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Gravity"

G = 2000

EARTH_VELOCITY = (0, 0)
MARS_VELOCITY = (0, 0)
VENUS_VELOCITY = (0, 0)
EARTH_MASS = 35
VENUS_MASS  = 50
MARS_MASS = 50
DEFAULT_MASS = 40

DEFAULT_RADIUS = 15

MAX_AMOUNT = 5




window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True)
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, 0

Earth = pymunk.Body(EARTH_MASS, 5)
Earth.position = 0.5*SCREEN_WIDTH, 0.*SCREEN_HEIGHT
Earth_shape = pymunk.Circle(Earth, 15)
Earth._set_velocity(EARTH_VELOCITY)


Mars = pymunk.Body(MARS_MASS, 50)
Mars.position = 0.4*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT
Mars_shape = pymunk.Circle(Mars, 20)
Mars._set_velocity(MARS_VELOCITY)


Venus = pymunk.Body(VENUS_MASS, 5)
Venus.position = 0.5*SCREEN_WIDTH, 0.75*SCREEN_HEIGHT
Venus_shape = pymunk.Circle(Venus, 25)
Venus._set_velocity(VENUS_VELOCITY)




space.add(Earth, Earth_shape, Mars, Mars_shape, Venus, Venus_shape)

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)

@window.event
def on_mouse_press(x, y, button, modifiers):

    if button == mouse.RIGHT:
        planet = pymunk.Body(DEFAULT_MASS*1000, 5)
        planet.position = x, y
        planet_shape = pymunk.Circle(planet, DEFAULT_RADIUS*5)
        space.add(planet, planet_shape)
    else:
        planet = pymunk.Body(DEFAULT_MASS, 5)
        planet.position = x, y
        planet_shape = pymunk.Circle(planet, DEFAULT_RADIUS)
        space.add(planet, planet_shape)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        for body in space.bodies:
            shape = body.shapes
            space.remove(shape)
            space.remove(body)

def Force(obj1, obj2):
    r = obj1.position - obj2.position
    output = -r * G * obj1.mass * obj2.mass / r.length ** 3
    return output

def update(dt):
    space.step(dt)
    for planet1 in space.bodies:
        for planet2 in space.bodies:
            if planet1 is not planet2:
                f12 = planet1._get_force() + Force(planet1, planet2)
                f21 = planet2._get_force() + Force(planet2, planet1)
                planet1._set_force(f12)
                planet2._set_force(f21)




if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
