from enum import Enum
import math
from random import Random
from typing import Type
from pyray import *
from raylib import DEFAULT, KEY_R, MOUSE_BUTTON_LEFT, TEXT_SIZE
from typing import TypeVar, Optional, Generic

# "Russian violet" hex="462255" r="70" g="34" b="85" />
# "Alice Blue" hex="e1f2fe" r="225" g="242" b="254" />
# "Vermilion" hex="ff3c38" r="255" g="60" b="56" />
# "Light green" hex="80ed99" r="128" g="237" b="153" />
# "Ultra Violet" hex="5b507a" r="91" g="80" b="122" />

RUSSIAN_VIOLET = Color(70,34,85,255)
ALICE_BLUE = Color(25,42,54,255)
VERMILION = Color(255,60,56, 255)
LIGHT_GREEN = Color(128,237,153, 255)
ULTRA_VIOLET = Color(91,80,122, 255)

NODE_COLOR_RED = VERMILION
NODE_COLOR_BLACK = ALICE_BLUE
NODE_COLOR_TEXT = LIGHT_GREEN
NODE_COLOR_LINE = RUSSIAN_VIOLET
BACKGROUND_COLOR = ULTRA_VIOLET


WIDTH = 1000
HEIGHT = 800
FONT_SIZE = 20
TEXTBOX_SIZE = 30

init_window(WIDTH, HEIGHT, "Red Black Tree")
set_target_fps(60)

T = TypeVar('T')
class NodeColor(Enum):
    NIL = 0
    BLACK = 1
    RED = 2

class TreeType(Enum):
    BINARY_SEARCH = 0
    RED_BLACK = 1

treeType = TreeType.RED_BLACK
class Node(Generic[T]): 
    def __init__(self, num:int = 0, color = NodeColor.RED, left: Optional["Node[T]"] = None, right: Optional["Node[T]"] = None) -> None:
        self.num = num
        self.color: NodeColor = color
        self.left = left
        self.right = right
        self.parent: Optional['Node[T]'] = None
    def depth(self) -> int:
        if self is None:
            return 0
        depth = 0
        if self.right is not None:
            depth = self.right.depth()
        if self.left is not None:
            depth = max(depth, self.left.depth())
        return depth + 1

    def insert_binary(self, node: Optional['Node[T]']):
        if node is None:
            return
        if node.num == self.num:
            return

        if node.num < self.num:
            if self.left is None:
                self.left = node
                node.parent = self
            else:
                self.left.insert_binary(node)
        else:
            if self.right is None:
                self.right = node
                node.parent = self
            else:
                self.right.insert_binary(node)


    def isRightChild(self) -> bool:
        return self.parent is not None and self.parent.right == self

    def getGrandParent(self) -> Optional['Node[T]']:
        return self.parent.parent if self.parent is not None else None

    def getUncle(self) -> Optional['Node[T]'] :
        if self.parent is None:
            return None
        grandParent = self.getGrandParent()
        if grandParent is None:
            return None
        if self.parent.isRightChild():
            return grandParent.left
        else:
            return grandParent.right 

    def fix_red_black(self):
        
        if self is None:
            return
        print(f"fixing with z: ${self.num} color ${self.color}")
        if self.parent is None:                   # case 1: node is the root
            print("Case 1")
            self.color = NodeColor.BLACK
            return
        if self.color == NodeColor.BLACK:
            self.parent.fix_red_black()
            return

        grandParent = self.getGrandParent()
        uncle = self.getUncle()
        print({ 'self': self.num, 'parent': self.parent.num if self.parent is not None else None, 'uncle': uncle.num if uncle is not None else None, 'grandParent': grandParent.num if grandParent is not None else None})
        if uncle is not None and uncle.color == NodeColor.RED: # case 2: Uncle color is RED
            print("Case 2")
            self.parent.color = NodeColor.BLACK
            uncle.color = NodeColor.BLACK
            if grandParent is not None: 
                grandParent.color = NodeColor.RED
            print({ 'self': self.color, 'parent': self.parent.color, 'uncle': uncle.color if uncle is not None else None, 'grandParent': grandParent.color if grandParent is not None else None})
            self.parent.fix_red_black()
            return

    def insert(self, node: Optional['Node[T]'] = None ):
        self.insert_binary(node)
        if node is not None:
            node.fix_red_black()
        print("\n")

root = None
root = Node(9, color=NodeColor.BLACK)

def update_state(num: (int|None) = None):
    global root, random
    if num is not None:
        if root is None:
            root = Node(num)
        else:
            root.insert(Node(num))


def draw_node(node: (Node|None), position: Vector2):
    if node == None:
        return
    gap = 80

    depth = node.depth()
    left_position = Vector2(position.x - (gap * depth * math.tanh(math.pi * 0.03 * depth )) , position.y + gap)
    right_position = Vector2(position.x + (gap * depth * math.tanh(math.pi * 0.03 * depth)), position.y + gap)

    if node.left is not None:
        draw_line_ex(position, left_position, 2, NODE_COLOR_LINE)
    if node.right is not None:
        draw_line_ex(position, right_position, 2, NODE_COLOR_LINE)
    text_size = measure_text(str(node.num), FONT_SIZE)
    node_color = NODE_COLOR_RED if node.color == NodeColor.RED else NODE_COLOR_BLACK
    draw_circle(int(position.x), int(position.y), 20, node_color)
    draw_text(str(node.num), int(position.x - text_size/2), int(position.y - FONT_SIZE/2.5), FONT_SIZE, NODE_COLOR_TEXT)

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



