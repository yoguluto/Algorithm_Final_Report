#Implementation of red-black tree
#Since the nodes in red-black tree have colors, 
#we can define a class to represent the nodes. 
#We saved the key (i.e., data), parent-child information and color in this class

class TreeNode(object):
    def __init__(self, data, left=None, right=None, parent=None, color="RED"):
        self.data = data # define the value of this node
        self.left = left # as an isolated node without left child
        self.right = right # as an isolated node without right child
        self.parent = parent # as an isolated node without parent
        self.color = color # the default color for a new node is red

class RBTree(object):
    def __init__(self):
        self.root = None
        self.size = 0
   
    def find(self, key, node = "ROOT"):# search function 
        """
        :param key: the key we want to find
        :return: the node as a callable object
        """
        if node =="ROOT":
            node = self.root
        if not node:
            return TreeNode("NotFound")
        elif key < node.data:
            return self.find(key, node.left)
        elif key > node.data:
            return self.find(key, node.right)
        else:
            return node
    
    def findMin(self, node):
        """
        find the minimum (left leaf) of one node
        :param node: the start node
        :return: the leaf as a callable object
        """
        temp_node = node
        while temp_node.left:
            temp_node = temp_node.left
        return temp_node
    
    def findMax(self, node):
        """
        find the maximum (right leaf) of one node
        :param node: the start node
        :return: the leaf as a callable object
        """
        temp_node = node
        while temp_node.right:
            temp_node = temp_node.right
        return temp_node
    
    def transplant(self, node_u, node_v): # replace function
        """
        reset the parent of u as the parent of v; used especially in deletion funcition
        :param node_u: the replaced node
        :param node_v: the replacing node
        :return: None
        """
        if not node_u.parent: # if node_u is the root
            self.root = node_v
        elif node_u == node_u.parent.left: #  if node_u is at left
            node_u.parent.left = node_v
        elif node_u == node_u.parent.right: # if node_u is at right
            node_u.parent.right = node_v
        # if v is none
        if node_v:
            node_v.parent = node_u.parent
    
    def left_rotate(self, node): # left rotation function
        #Note that the rotation happens between nodes and its left child
        '''
            :param node: the node where left rotation happaned
            :return: None
        '''
        parent = node.parent
        right = node.right
        # rotate
        node.right = right.left
        if node.right: # reset the parent of the node's right child
            node.right.parent = node
        #set node as the left child of its (previous) right child
        right.left = node
        #set node’s parent as its (previous) right child
        node.parent = right
        #set the parent of node’s (previous) right child as the parent of the node
        right.parent = parent
        #set the child information for the parent node
        if not parent:
            self.root = right
        else:
            if parent.left == node:
                parent.left = right
            else:
                parent.right = right
    
    def right_rotate(self, node):
        # Note that the rotation happens between nodes and its left child
        '''
            :param node:
            :return: None
        '''
        parent = node.parent
        left = node.left
        # rotate
        node.left = left.right
        if node.left: # reset the parent of the node's left child
            node.left.parent = node
        #set node as the right child of its (previous) left child
        left.right = node
        #set node’s parent as its (previous) left child
        node.parent = left
        #set the parent of node’s (previous) left child as the parent of the node
        left.parent = parent
        #set the child information for the parent node
        if not parent:
            self.root = left
        else:
            if parent.left == node:
                parent.left = left
            else:
                parent.right = left
    
    def insert(self, node):
        """
        :param node: the new node for insertion
        :return: None
        """
        temp_root = self.root
        temp_node = None
        while temp_root: # if the tree is not empty
            temp_node = temp_root
            # if the node existed, it will not be inserted again.
            if node.data == temp_node.data:
                print("Node has existed") 
                return
            # binary search
            elif node.data > temp_node.data:
                temp_root = temp_root.right
            else:
                temp_root = temp_root.left
        
        # insert at the corresponding position
        if not temp_node: # temp_node is None. It means the tree is empty
            # Case 1 for insertion
            self.root = node
            node.color = "BLACK"
        elif node.data < temp_node.data:
            temp_node.left = node
            node.parent = temp_node
        else:
            temp_node.right = node
            node.parent = temp_node
        #adjust the tree to keep property 4 and 5
        self.insert_fixup(node)
    
    def insert_fixup(self, node):# adjustment for insertion
        """
        :param: the new node which is inserted
        :return: None
        """
        if node.data == self.root.data: # Case 1, the new node is root
            return
        
        while node.parent and node.parent.color == "RED":
            # enter into the loops only when the parent node is red
            # will not enter into loops in Case 2 of insertion 
            if node.parent == node.parent.parent.left: #the parent node on the left
                node_uncle = node.parent.parent.right
                
                if node_uncle and node_uncle.color == "RED": # Case 3.1. in insertion
                    
                    node.parent.color = "BLACK" #recolor
                    node_uncle.color = "BLACK" #recolor
                    node.parent.parent.color = "RED" #recolor
                    node = node.parent.parent # move to higher layer
                    continue # enter into the while loop again to check higher layers
                elif node == node.parent.right: # Case 3.3.1 
                    # the uncle node is black 
			        #the parent node on the left
			        # the new node on the right
                    self.left_rotate(node.parent) #do left rotation
                    node = node.left # set the situation as same as Case 3.3.

                 #Case 3.3.
                node.parent.color = "BLACK" # since the parent-child information will change, recolor firstly
                node.parent.parent.color = "RED" 
                self.right_rotate(node.parent.parent) # do right rotation
                return # stop the adjustment
            
            # symmetric situation
            elif node.parent == node.parent.parent.right: #the parent node on the right
                node_uncle = node.parent.parent.left
                if node_uncle and node_uncle.color == "RED": # Case 3.1. in insertion
                    node.parent.color = "BLACK" #recolor
                    node_uncle.color = "BLACK" #recolor
                    node.parent.parent.color = "RED" #recolor
                    node = node.parent.parent #move to higher layers
                    continue # enter into the while loop again to check higher layers
                elif node == node.parent.left: # Case 3.2.1 
                    # the uncle node is black 
			        # the parent node on the right
			        # the new node on the left
                    self.right_rotate(node.parent) #do right rotation
                    node = node.right # set the situation as same as Case 3.2.
                
                #Case 3.2.
                node.parent.color = "BLACK" # since the parent-child information will change, recolor firstly
                node.parent.parent.color = "RED"
                self.left_rotate(node.parent.parent) # do left rotation
                return # stop the adjustment
        
        #After jumping out of the while loop
        #reset the root as black to ensure property 2
        self.root.color = "BLACK"
    
    def delete(self, key):
        """
        :param: the key of the deleted node
        :return: None
        """
        node = self.find(key) # find the address of the node
        if node.data == "NotFound": # if not existed, return
            return
        
        node_color = node.color # save the node of the node for check
        
        #if node has less than two children
        if not node.left:#no left child
            if not node.right: #if the node without any child
                node.right = TreeNode("NIL") # use NIL to replace
                node.right.parent = node
                node.right.color = "BLACK" #NIL is always black
            temp_node = node.right # save the replacing node
            self.transplant(node, node.right) # replace the node
        
        elif not node.right: #no right child
            #if not node.left:
            #    node.left = TreeNode("NIL")
            #    node.left.parent = node
            #    node.left.color = "BLACK"

            temp_node = node.left # save the replacing
            self.transplant(node, node.left) # replace the node
        
        else:
            # the node has two children
            node_min = self.findMin(node.right) #find left leaf of right subtree
            #finally we will exchange node_min with node, so we need to update color
            node_color = node_min.color
            if not node_min.right: # if node_min has no child
                node_min.right = TreeNode("NIL")
                node_min.right.parent = node_min
                node_min.right.color = "BLACK"
            
            temp_node = node_min.right #save the replacing node
            #if node_min is a child of node, we can replace the node directly
            if node_min.parent != node: #if node_min is not a child of node
                self.transplant(node_min, node_min.right) #reassign the parent of node_min to node_min.right
                node_min.right = node.right # reset the right child of node as the right child of node_min; Note node_min is the left leaf in the right subtree
                node_min.right.parent = node_min 
            self.transplant(node, node_min) #reassign the parent of node to node_min
            node_min.left = node.left # reset the relathionship of the left child
            node_min.left.parent = node_min
            #by above way, we delete the node and move node_min to the position of the node
            #so in summary, we delete a node with key of the node but at position of node_min with node_min's color  
            node_min.color = node.color # reset the color of node_min
            
            
        # if we delete a black node, we need to adjust
        if node_color == "BLACK":
            self.delete_fixup(temp_node)
        else:# we do not want to show a NIL node in our tree, so we delete the NIL which is possible to show.
            if temp_node.data == "NIL":
                if temp_node == temp_node.parent.left:
                    temp_node.parent.left = None
                else:
                    temp_node.parent.right = None
    
    def delete_fixup(self, node):# Note here node represents the replacing node
        """
        :param: the replacing node as a callable object
        :return: None
        """
        temp_node = node # save the replacing node
        
        while node != self.root and node.color == "BLACK":
            
            if node == node.parent.left: #the replacing node is at left
                node_brother = node.parent.right
                if node_brother.color == "RED": #Case 3.1.1
                    node_brother.color = "BLACK" # Recolor
                    node.parent.color = "RED" # Recolor
                    self.left_rotate(node.parent) # left rotation
                    node_brother = node.parent.right # relocated brother
                    #The while loop make us to check the higher layer until meet the root

                if (not node_brother.left or node_brother.left.color == "BLACK") and (not node_brother.right or node_brother.right.color == "BLACK"):
                    # Case 3.1.4
                    node_brother.color = "RED" # recolor
                    node = node.parent # move to higher layers
                    #continue
                else:
                    if not node_brother.right or node_brother.right.color == "BLACK":
                        # Case 3.1.3; shift this situation to Case 3.1.2
                        node_brother.color = "RED" # Recolor
                        node_brother.left.color = "BLACK" # Recolor
                        self.right_rotate(node_brother) # right rotation
                        node_brother = node.parent.right # relocate
                        #Shift finished

                    # Case 3.1.2
                    node_brother.color = node.parent.color # Recolor
                    node.parent.color = "BLACK" # Recolor
                    node_brother.right.color = "BLACK" # Recolor
                    self.left_rotate(node.parent) # Left rotation
                    node = self.root # if we finished the adjustment of 3.1.2, we can ensure the whole tree maintains all properties; Therefore we return to the root
                    break # Then we break the loop

            else: #the replacing node is at right
                node_brother = node.parent.left
                if node_brother.color == "RED": #Case 3.2.1
                    node_brother.color = "BLACK" # Recolor
                    node.parent.color = "RED" # Recolor
                    self.right_rotate(node.parent) # Right rotation
                    node_brother = node.parent.left # relocate brother node
                    #The while loop make us to check the higher layer until meet the root
                     
                if (not node_brother.left or node_brother.left.color == "BLACK") and (not node_brother.right or node_brother.right.color == "BLACK"):
                    # Case 3.2.4
                    node_brother.color = "RED" # recolor
                    node = node.parent # move to higher layers
                    #continue
                else:
                    if not node_brother.left or node_brother.left.color == "BLACK":
                        # Case 3.2.3; shift this situation to Case 3.2.2
                        node_brother.color = "RED" # Recolor
                        node_brother.right.color = "BLACK" # Recolor
                        self.left_rotate(node_brother) # left rotation
                        node_brother = node.parent.left  # relocate
                        #Shift finished
                    
                    # Case 3.2.2
                    node_brother.color = node.parent.color # Recolor
                    node.parent.color = "BLACK" # Recolor 
                    node_brother.left.color = "BLACK" # Recolor
                    self.right_rotate(node.parent) # Right rotation
                    node = self.root # if we finished the adjustment of 3.2.2, the whole tree maintains all properties; Therefore we return to the root
                    break # Then we break the loop

        node.color = "BLACK" # set the root to black
        
        if temp_node.data == "NIL": # if the replacing node is NIL, we do not want show it in the tree; so we delete it
            if temp_node == temp_node.parent.left:
                temp_node.parent.left = None
            else:
                temp_node.parent.right = None



#Test code
#Test the effectiveness of the insertion between red-black tree and AVL tree
import random
import time
import sys
from AVLTree import *
from DrawTree import *

i = 0
N = 100 # average time of 100 trees
Num_node = 100 # number of inserted nodes
TimeComplexity_RB = []
TimeComplexity_AVL = []

while i < N:
    randomlist = random.sample(range(10**7), Num_node)
    rbtree =RBTree()
    avltree = AVLTree()
    
    t1 = time.time()
    for i in randomlist: 
        rbtree.insert(TreeNode(i))
    t2 = time.time()
    
    t3 = time.time()
    for i in randomlist: #data:
        avltree.insert(i)
    t4 = time.time()
    
    TimeComplexity_RB.append(t2-t1)
    TimeComplexity_AVL.append(t4-t3)

print(sum(TimeComplexity_AVL)/N)
print(sum(TimeComplexity_RB)/N)

# build one certain tree
#data = [5, 14, 16, 3, 18, 2, 9, 15, 6, 17, 10, 19, 4, 1, 12, 8, 7, 11, 13,20,22,26,28,30,33,40,36,35,39]

#rbtree =RBTree()
#for i in data: 
#    rbtree.insert(TreeNode(i))
#show_rb_tree(rbtree)

#rbtree.delete(14)
#rbtree.delete(6)

#show_rb_tree(rbtree)

#rbtree.delete(8)
#show_rb_tree(rbtree)
#rbtree.delete(14)
#show_rb_tree(rbtree)
#rbtree.delete(13)
#rbtree.delete(9)
#rbtree.delete(18)
#show_rb_tree(rbtree)
#show_rb_tree(rbtree)
#print(rbtree.find(5).data)
#print(rbtree.find(100).data)
#print(rbtree.find(101,rbtree.root).data)