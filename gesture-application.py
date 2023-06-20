# application for task 3
from time import sleep
import pyglet
from pyglet.gl import glClearColor
from recognizer import DollarRecognizer, Point
from pynput.keyboard import Key, Controller

window = pyglet.window.Window(250, 250)
glClearColor(1, 1, 1, 1)  # from chatGPT

pixels = []
points = []

recog = DollarRecognizer()

keyboard = Controller()


# from prev assignment
def apply_input():

    input_result = recog.recognize(points)
    input_condition = input_result.Name
    if input_condition == "triangle":
        pyglet.app.exit()
    elif input_condition == "caret":
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        print("volume up")
        sleep(0.3)
    elif input_condition == "v":
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        print("volume down")
        sleep(0.3)
    elif input_condition == "rectangle":
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
        print("stop/go")
        sleep(0.3)
    elif input_condition == "arrow":
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
        print("arrow")
        sleep(0.3)


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
        apply_input()
    pixels = []
    points = []


@window.event
def on_draw():
    window.clear()
    for pixel in pixels:
        pixel.draw()


pyglet.app.run()

