from enum import Enum
import math
from pyray import *
from raylib import DEFAULT, KEY_R, KEY_Z, MOUSE_BUTTON_LEFT, TEXT_SIZE
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


WIDTH = 1900
HEIGHT = 1020
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

class Drawable(object):
    def draw(self, at: Vector2):
        pass

class DrawableGeneric(Generic[T]):
    def draw(self, at: Vector2):
        pass

treeType = TreeType.BINARY_SEARCH
class Node(DrawableGeneric[T]): 
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

    def __str__(self) -> str:
        return f"""{self.num}:{self.color}->{self.parent}"""
    
    def rightRotate(self):
        print(f"right rotate: {self}")
        global root

        parent = self.parent
        left = self.left 
        isRoot = self.parent is None
        isRightChild = self.isRightChild()

        print(f"isRoot {isRoot}")
        if left is None: 
            print(f"root: {root}")
            return
        
        leftsRightChild = left.right


        # Cut self and left child
        self.right = None
        left.parent = None
        print(f"After cutting self {self} and right {left}")

        self.parent = None
        if parent is not None:
            if isRightChild:
                parent.right = None
            else:
                parent.left = None
        # cut leftChild and its right child
        left.right = None
        if leftsRightChild is not None:
            leftsRightChild.parent = None
        print(f"After cutting left: {left} and left's right {leftsRightChild}")

        # Setting rightsRight child to the right
        self.left = leftsRightChild
        if leftsRightChild is not None:
            leftsRightChild.parent = self

        print(f"After Setting self.right to leftsRightChild: {leftsRightChild} {self}")

        # Set up right as parent for self
        left.right = self
        self.parent = left

        print(f"After Setting self as lefts right, self:{self} right: {left}")
        # Set up the rightChild with self's parent
        if isRoot or parent is None:
            root = left
            print(f"root: {root}")
            return
        if isRightChild:
            parent.right = left
        else:
            parent.left = left
        left.parent = parent
        
        print(f"after all rotation left: {left}, self: {self}")
        print(f"root: {root}")
        self.fix_red_black()
        
    def leftRotate(self):
        print(f"left rotate: {self}")
        global root

        parent = self.parent
        right = self.right 
        isRoot = self.parent is None
        isRightChild = self.isRightChild()

        print(f"isRoot {isRoot}")
        if right is None: 
            print(f"root: {root}")
            return
        
        rightsLeftChild = right.left


        # Cut self and right child
        self.right = None
        right.parent = None

        self.parent = None
        if parent is not None:
            if isRightChild:
                parent.right = None
            else:
                parent.left = None
        print(f"After cutting self {self} and right {right}")

        # cut rightChild and its right child
        right.left = None
        if rightsLeftChild is not None:
            rightsLeftChild.parent = None
        print(f"After cutting right {right} and right's left {rightsLeftChild}")

        # Setting rightsRight child to the right
        self.right = rightsLeftChild
        if rightsLeftChild is not None:
            rightsLeftChild.parent = self

        print(f"Setting self.right to rightsLeftChild: {rightsLeftChild} {self}")

        # Set up right as parent for self
        right.left = self
        self.parent = right

        print(f"Setting self as right's left, self:{self} right: {right}")
        # Set up the rightChild with self's parent
        if isRoot or parent is None:
            root = right
            print(f"root: {root}")
            return
        if isRightChild:
            parent.right = right
        else:
            parent.left = right
        right.parent = parent

        print(f"after all rotation right: {right}, self: {self}")
        print(f"root: {root}")
        self.fix_red_black()

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

        print(f"fixup {self}")
        if self is None:
            return
        if self.parent is None:                   # case 1: node is the root
            print("Case 1")
            self.color = NodeColor.BLACK
            return
        if self.color == NodeColor.BLACK:
            self.parent.fix_red_black()
            return
        elif not self.parent.color == NodeColor.RED and (self.left is None or self.left.color == NodeColor.BLACK) and (self.right is None or self.right.color == NodeColor.BLACK):
            self.parent.fix_red_black()
            return

        grandParent = self.getGrandParent()
        uncle = self.getUncle()
        print(f"checking conditions {self}, uncle: {uncle}")
        if uncle is not None and uncle.color == NodeColor.RED: # case 2: Uncle color is RED
            print("Case 2")
            self.parent.color = NodeColor.BLACK
            uncle.color = NodeColor.BLACK
            if grandParent is not None: 
                grandParent.color = NodeColor.RED
            print(f"After fixing case 2 {self}, uncle: {uncle}")
            self.parent.fix_red_black()
            return
        else:                                               # case 3: Uncle color is BLACK
            print("Case 3")
            if grandParent is None:
                return
            if not self.isRightChild() == self.parent.isRightChild(): # case 3: Uncle color is BLACK (triangle)
                print("Triangle")
                if self.isRightChild():
                    self.parent.leftRotate()
                else:
                    self.parent.rightRotate()
            else:
                print("Line")
                parent = self.parent
                gpColor = grandParent.color
                grandParent.color = parent.color
                parent.color = gpColor
                if self.isRightChild():
                    grandParent.leftRotate()
                else:
                    grandParent.rightRotate()

    def insert(self, node: Optional['Node[T]'] = None ):
        self.insert_binary(node)
        global treeType
        if node is not None:
            if treeType == TreeType.RED_BLACK:
                print("fixing red black tree")
                node.fix_red_black()
            else:
                node.color = NodeColor.BLACK
        print("\n")

    def draw(self, at: Vector2):
        if self == None:
            return
        gap = 80

        depth = self.depth()
        left_position = Vector2(at.x - (gap * depth * math.tanh(math.pi * 0.03 * depth )) , at.y + gap)
        right_position = Vector2(at.x + (gap * depth * math.tanh(math.pi * 0.03 * depth)), at.y + gap)

        if self.left is not None:
            draw_line_ex(at, left_position, 2, NODE_COLOR_LINE)
        if self.right is not None:
            draw_line_ex(at, right_position, 2, NODE_COLOR_LINE)
        text_size = measure_text(str(self.num), FONT_SIZE)
        node_color = NODE_COLOR_RED if self.color == NodeColor.RED else NODE_COLOR_BLACK
        draw_circle(int(at.x), int(at.y), 20, node_color)
        draw_text(str(self.num), int(at.x - text_size/2), int(at.y - FONT_SIZE/2.5), FONT_SIZE, NODE_COLOR_TEXT)

        if self.left is not None:
            self.left.draw(left_position)
        if self.right is not None:
            self.right.draw(right_position)

root = None
# root = Node(1, color=NodeColor.BLACK)
# for i in range(1,10):
#     root.insert(Node(i))

def update_state(num: (int|None) = None):
    global root, random, treeType
    if num is not None:
        if root is None:
            root = Node(num)
            if treeType == TreeType.RED_BLACK:
                root.fix_red_black()
        else:
            root.insert(Node(num))


camera = Camera2D(Vector2(0,0), Vector2(0,0), 0.0, 1.0)
value = 0
editable = True
gui_set_style(DEFAULT, TEXT_SIZE, FONT_SIZE)
while not window_should_close():
    if int(get_time()) % 10 == 0:
        update_state()

    if is_key_down(KEY_R):
        root = None
    if is_key_down(KEY_Z):
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
    if treeType == TreeType.RED_BLACK:
        if gui_button(Rectangle(540, 10, 230, 50), "RedBlack Tree") != 0:
            treeType = TreeType.BINARY_SEARCH
    elif treeType == TreeType.BINARY_SEARCH:
        if gui_button(Rectangle(540, 10, 230, 50), "Binary Search Tree") != 0:
            treeType = TreeType.RED_BLACK
    clear_background(GRAY)

    begin_mode_2d(camera)
    if root is not None:
        root.draw(Vector2(int(WIDTH/2), int(HEIGHT/2)))
    end_mode_2d()

    draw_text("Press (Z) to reset zoom. (R) to reset tree", 20, HEIGHT - 50, 20, DARKGRAY)

    end_drawing()

