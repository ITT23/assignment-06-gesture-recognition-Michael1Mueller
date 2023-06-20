# gesture input program for first task
import pyglet
from pyglet.gl import glClearColor
from recognizer import DollarRecognizer, Point

window = pyglet.window.Window(250, 250)
glClearColor(1, 1, 1, 1)  # from chatGPT

pixels = []
points = []

recog = DollarRecognizer()

label = pyglet.text.Label(text="Mögliche Zeichen: ->, ▭, v, ^, △", x=10, y=235, font_size=12, color=(0, 0, 0, 255))
prediction_label = pyglet.text.Label(text="Prediction: ", x=10, y=215, font_size=12, color=(0, 0, 0, 255))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    rectangle = pyglet.shapes.Rectangle(x, y, 1, 1, color=(255, 0, 0))
    pixels.append(rectangle)
    points.append(Point(x, y))


def predict(pts):
    prediction = recog.recognize(pts)
    if prediction.Name == "v":
        prediction_label.text = "Prediction: v"
    elif prediction.Name == "caret":
        prediction_label.text = "Prediction: ^"
    elif prediction.Name == "rectangle":
        prediction_label.text = "Prediction: ▭"
    elif prediction.Name == "arrow":
        prediction_label.text = "Prediction: ->"
    elif prediction.Name == "triangle":
        prediction_label.text = "Prediction: △"


@window.event
def on_mouse_press(x, y, button, modifiers):
    global pixels
    global points
    if button == pyglet.window.mouse.LEFT:
        pixels = []
        points = []


@window.event
def on_mouse_release(x, y, button, modifiers):
    if len(points) > 0:
        predict(points)


@window.event
def on_draw():
    window.clear()
    label.draw()
    prediction_label.draw()
    for pixel in pixels:
        pixel.draw()


pyglet.app.run()
