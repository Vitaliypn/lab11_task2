"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root
        while node:
            if item == node.data:
                return True
            elif item < node.data:
                node = node.left
            else:
                node = node.right
        return False

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return

        # Helper function to search for item's position
        node = self._root
        while True:
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                    self._size += 1
                    break
                else:
                    node = node.left
            # New item is greater or equal, go right until spot is found
            else:
                if node.right is None:
                    node.right = BSTNode(item)
                    self._size += 1
                    break
                else:
                    node = node.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        probe = self._root
        return self.height1(probe)
    def height1(self, top):
        '''
        Helper function
        :param top:
        :return:
        '''
        if top.left is None and top.right is None:
            return 0
        else:
            return 1 + max(self.height1(c) for c in [x for x in [top.left, top.right]if x is not None])

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        count = 0
        for item in self.inorder():
            count +=1
        return self.height() < 2 * log(1 + count, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = []
        for item in self.inorder():
            res.append(item)
        return [x for x in res if low <= x <= high]


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = list(self.inorder())
        self.clear()
        def balance(lst):
            if len(lst) <= 1:
                return lst
            mid = len(lst) // 2
            root = [lst[mid]]
            left = balance(lst[:mid])
            right = balance(lst[mid+1:])
            return root + left + right
        for elem in balance(nodes):
            self.add(elem)
        return balance(nodes)
            

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        current = self._root
        successor = None

        while current is not None:
            if current.data > item:
                successor = current.data
                current = current.left
            else:
                current = current.right
        return successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        current = self._root
        predecessor = None

        while current is not None:
            if current.data < item:
                predecessor = current.data
                current = current.right
            else:
                current = current.left
        return predecessor

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = []
        with open(path, mode='r',encoding='utf-8') as file:
            lines = file.readlines()
            prob = 10000/len(lines)
            for line in lines:
                if random.random() < prob:
                    words.append(line.strip())
        not_shuffle = list(tuple(words))
        random.shuffle(words)
        print(f'Running time for search 10000 words in list: {self.list_search(words, not_shuffle)}')
        self.create_tree(not_shuffle)
        print(f'Running time for search 10000 words in sorted tree: {self.find_all(not_shuffle)}')
        self.create_tree(words)
        print(f'Running time for search 10000 words in random created tree: {self.find_all(not_shuffle)}')
        self.rebalance()
        print(f'Running time for search 10000 words in balance tree: {self.find_all(not_shuffle)}')

    def list_search(self,first, second):
        """Searching with list"""
        start_time = time.time()
        for element in first:
            i = 0
            for elem in second:
                i += 1
                if element == elem:
                    break
        end_time = time.time()
        return  end_time - start_time

    def create_tree(self, lst):
        """Creating a tree based on a list"""
        self.clear()
        for element in lst:
            self.add(element)

    def find_all(self, lst):
        """Finding all the elements"""
        start_time = time.time()
        for element in lst:
            self.find(element)
        end_time = time.time()
        return end_time - start_time

a = LinkedBST()
a.demo_bst('words.txt')
                