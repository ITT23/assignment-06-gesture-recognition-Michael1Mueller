# gesture input program for first task
import pyglet
from pyglet.gl import glClearColor
from recognizer import DollarRecognizer, Point

window = pyglet.window.Window(250, 250)
glClearColor(1, 1, 1, 1)  # from chatGPT

pixels = []
points = []

recog = DollarRecognizer()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    rectangle = pyglet.shapes.Rectangle(x, y, 1, 1, color=(255, 0, 0))
    pixels.append(rectangle)
    points.append(Point(x, y))


@window.event
def on_mouse_release(x, y, button, modifiers):
    global pixels
    global points
    if len(points) > 0:
        bruh = recog.recognize(points)
        print(bruh.Name)
    pixels = []
    points = []


@window.event
def on_draw():
    window.clear()
    for pixel in pixels:
        pixel.draw()


pyglet.app.run()
