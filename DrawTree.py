### code to draw the tree
### build based on the reference
### Reference https://github.com/jerome126/rbtree/blob/master/tree_plt.py　
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np

def get_left_length(node):
    if not node:
        return 0
    if not node.left:
        return 1
    if not node.right:
        return 2 + get_left_length(node.right)
    return 2 + get_left_length(node.left)


def get_right_length(node):
    if not node:
        return 0
    return 1 + get_right_length(node.right)

def get_height(node):
    if not node:
        return 0
    return 1 + max([get_height(node.left), get_height(node.right)])

def get_node_count(node):
    if not node:
        return 0
    return 1 + get_node_count(node.left) + get_node_count(node.right)


def get_fontsize(count):
    if count < 10:
        return 30
    if count < 20:
        return 20
    return 16


def show_node(node, ax, height, index, font_size):
    if not node:
        return
    x1, y1 = None, None
    if node.left:
        x1, y1, index = show_node(node.left, ax, height-1, index, font_size)
    x = 100 * index - 50
    y = 100 * height - 50
    if x1:
        plt.plot((x1, x), (y1, y), linewidth=2.0,color='b')
    circle_color = "black" if node.color == "BLACK" else 'r'
    text_color = "beige" if node.color == "BLACK" else 'black'
    ax.add_artist(plt.Circle((x, y), 50, color=circle_color))
    ax.add_artist(plt.Text(x, y, node.data, color= text_color, fontsize=font_size, horizontalalignment="center",verticalalignment="center"))
    # print(str(node.val), (height, index))

    index += 1
    if node.right:
        x1, y1, index = show_node(node.right, ax, height-1, index, font_size)
        plt.plot((x1, x), (y1, y), linewidth=2.0, color='b')

    return x, y, index

def draw_node_line(node, ax, height, index):
    x1, y1 = None, None
    if node.left:
        x1, y1, index = draw_node_line(node.left, ax, height-1, index)
    x = 100 * index - 50
    y = 100 * height - 50
    if x1:
        plt.plot((x1, x), (y1, y), linewidth=2.0,color='b')
    index += 1
    if node.right:
        x1, y1, index = draw_node_line(node.right, ax, height-1, index)
        plt.plot((x1, x), (y1, y), linewidth=2.0, color='b')

    return x, y, index

def show_rb_tree(tree):
    fig, ax = plt.subplots()
    left, right, height = get_left_length(tree.root), get_right_length(tree.root), get_height(tree.root)
    # print(left, right, height)
    plt.ylim(0, height*100+100)
    plt.xlim(0, 100 * get_node_count(tree.root) + 100)
    show_node(tree.root, ax, height, 1, get_fontsize(get_node_count(tree.root)))
    plt.show()