from pyray import *
from raylib import MOUSE_BUTTON_LEFT

WIDTH = 1000
HEIGHT = 800

init_window(WIDTH, HEIGHT, "Red Black Tree")

set_target_fps(60)

camera = Camera2D(Vector2(0,0), Vector2(0,0), 0.0, 1.0)
while not window_should_close():
    if get_mouse_wheel_move() != 0:
        camera.zoom += 0.1 * get_mouse_wheel_move()
        camera.target = get_screen_to_world_2d(get_mouse_position(), camera)
        camera.offset = get_mouse_position()
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        delta = vector2_scale(get_mouse_delta(), -1.0/camera.zoom)
        camera.target = vector2_add(camera.target, delta)
    begin_drawing()

    clear_background(GRAY)

    begin_mode_2d(camera)
    draw_circle(int(WIDTH/2), int(HEIGHT/2), 20, RED)
    end_mode_2d()

    end_drawing()



