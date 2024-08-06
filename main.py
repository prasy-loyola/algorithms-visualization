from enum import Enum
import math
from random import Random
from pyray import *
from raylib import DEFAULT, KEY_R, MOUSE_BUTTON_LEFT, TEXT_SIZE


WIDTH = 1000
HEIGHT = 800
FONT_SIZE = 20
TEXTBOX_SIZE = 30

init_window(WIDTH, HEIGHT, "Red Black Tree")
set_target_fps(60)

class NodeColor(Enum):
    NIL = 0
    BLACK = 1
    RED = 2

class Node(object): 
    def __init__(self, num:int = 0, color = NodeColor.NIL, left = None, right = None) -> None:
        self.num = num
        self.color: NodeColor = color
        self.left: (Node| None) = left
        self.right: (Node|None) = right
    def depth(self) -> int:
        if self is None:
            return 0
        depth = 0
        if self.right is not None:
            depth = self.right.depth()
        if self.left is not None:
            depth = max(depth, self.left.depth())
        return depth + 1

    def insert(self, node = None ):
        if node is None:
            return
        if node.num == self.num:
            return

        if node.num < self.num:
            if self.left is None:
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                self.right = node
            else:
                self.right.insert(node)


root = None
random = Random()
root = Node(9)
root.insert(Node(5))
root.insert(Node(15))
root.insert(Node(10))

def update_state(num: (int|None) = None) -> bool:
    global root, random
    if num is not None:
        if root is None:
            root = Node(num)
        else:
            root.insert(Node(num))
    return num is not None and num < 50

def draw_node(node: (Node|None), position: Vector2):
    if node == None:
        return
    gap = 100

    depth = node.depth()
    left_position = Vector2(position.x - (gap * depth * math.tanh(math.pi * 0.03 * depth )) , position.y + gap)
    right_position = Vector2(position.x + (gap * depth * math.tanh(math.pi * 0.03 * depth)), position.y + gap)

    if node.left is not None:
        draw_line_ex(position, left_position, 2, BLUE)
    if node.right is not None:
        draw_line_ex(position, right_position, 2, BLUE)
    text_size = measure_text(str(node.num), FONT_SIZE)
    node_color = RED if node.color == NodeColor.RED else BLACK
    draw_circle(int(position.x), int(position.y), 20, node_color)
    draw_text(str(node.num), int(position.x - text_size/2), int(position.y - FONT_SIZE/2.5), FONT_SIZE, YELLOW)

    draw_node(node.left, left_position)
    draw_node(node.right, right_position)

camera = Camera2D(Vector2(0,0), Vector2(0,0), 0.0, 1.0)
value = 0
editable = True
gui_set_style(DEFAULT, TEXT_SIZE, FONT_SIZE)
while not window_should_close():
    if int(get_time()) % 10 == 0:
        update_state()

    if is_key_down(KEY_R):
        camera.zoom = 1.0
        camera.offset = Vector2(0,0)
        camera.target = Vector2(0,0)
    if get_mouse_wheel_move() != 0:
        camera.zoom += 0.2 * get_mouse_wheel_move()
        camera.target = get_screen_to_world_2d(get_mouse_position(), camera)
        camera.offset = get_mouse_position()
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        delta = vector2_scale(get_mouse_delta(), -1.0/camera.zoom)
        camera.target = vector2_add(camera.target, delta)
    begin_drawing()
    draw_text(str(value), 10, 15, 40, BLACK)
    if gui_button(Rectangle(60, 10, 40, 50), "-"):
        value -= 1
    if gui_button(Rectangle(100, 10, 40, 50), "+"):
        value += 1
    if gui_button(Rectangle(140, 10, 40, 50), "Add") != 0:
        update_state(int(value))

    clear_background(GRAY)

    begin_mode_2d(camera)
    draw_node(root,Vector2(int(WIDTH/2), int(HEIGHT/2)))
    end_mode_2d()

    end_drawing()



