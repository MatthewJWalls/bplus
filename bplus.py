#!/usr/bin/env python

debugMode = False

import sys

def debug(s):
    if debugMode:
        print s

class Node:

    def __init__(self, parent=None, prevNode=None, nextNode=None):
        self.parent   = parent
        self.children = []
        self.keys     = []
        self.prevNode = prevNode
        self.nextNode = nextNode

    def __str__(self):
        return "node:<%s>" % self.keys

class Tree:
    
    def __init__(self):
        self.root = Node()
        self.threshold = 2 # this is hard coded for now

    def overflow(self, node):
        """ overflows a node """

        debug("overflowing node %s with parent %s" % (node, node.parent))
        assert len(node.keys) > self.threshold

        keys = node.keys

        if not node.children:

            # is leaf

            debug ("  is leaf")

            if not node.parent:
                debug("  Creating parent and resetting root")
                node.parent = Node(None)
                self.root = node.parent

            lnode = Node(node.parent)
            rnode = Node(node.parent)

            lnode.prevNode = node.prevNode
            lnode.nextNode = rnode
            rnode.prevNode = lnode
            rnode.nextNode = node.nextNode

            if node.prevNode:
                node.prevNode.nextNode = lnode

            if node.nextNode:
                node.nextNode.prevNode = rnode

            insertPosition = 0

            if node in node.parent.children:
                insertPosition = node.parent.children.index(node)
                node.parent.children.remove(node)

            node.parent.children.insert(insertPosition, rnode)
            node.parent.children.insert(insertPosition, lnode)

            lnode.keys.append(keys[0])
            rnode.keys.append(keys[1])
            rnode.keys.append(keys[2])

            hoist = keys[1]
            node.parent.keys.append(hoist)
            node.parent.keys.sort()

            if len(node.parent.keys) > self.threshold:
                debug("  I noticed my parent looks like %s, so I am overflowing" % node.parent)
                self.overflow(node.parent)

        elif node == self.root:

            # I am root

            debug("  is root")

            # My keys will look like [A|B|C]

            newroot = Node(None)
            newroot.keys.append(keys[1])

            lnode = Node(newroot)
            rnode = Node(newroot)

            lnode.keys.append(keys[0])
            rnode.keys.append(keys[2])

            for child in node.children[:2]:
                lnode.children.append(child)
                child.parent = lnode

            for child in node.children[2:]:
                rnode.children.append(child)
                child.parent = rnode

            newroot.children.append(lnode)
            newroot.children.append(rnode)

            newroot.keys.sort()

            self.root = newroot

        else:

            # internal node

            debug("  internal node")

            lnode = Node(node.parent)
            rnode = Node(node.parent)
            
            lnode.keys.append(keys[0])
            rnode.keys.append(keys[2])
            
            for child in node.children[:2]:
                lnode.children.append(child)
                child.parent = lnode

            for child in node.children[2:]:
                rnode.children.append(child)
                child.parent = rnode

            if node in node.parent.children:
                insertPosition = node.parent.children.index(node)
                node.parent.children.remove(node)

            node.parent.children.insert(insertPosition, rnode)
            node.parent.children.insert(insertPosition, lnode)

            hoist = keys[1]
            node.parent.keys.append(hoist)
            node.parent.keys.sort()

            if len(node.parent.keys) > self.threshold:
                self.overflow(node.parent)

    def find(self, val, node=None):

        # recurse down the right tree path until we hit the
        # leaf node that the value should be in, then return
        # a tuple, t, where t[0] is True or False depending on
        # whether the value was found, and t[1] is the leaf
        # node where the value _should_ have been.

        if node is None:
            node = self.root

        if node.children:

            # non-leaf, we need to work out what child to
            # descend to, and then recurse

            nodeToDescend = 0

            for i, k in enumerate(node.keys):
                if val < k:
                    break
                else:
                    nodeToDescend += 1

            return self.find(val, node.children[nodeToDescend])
                    
        else:

            # leaf

            if val in node.keys:
                # found it
                return (True, node)
            else:
                # it's not in the tree
                return (False, node)

    def insert(self, val):

        found, node = self.find(val)
        assert node is not None

        if found:
            return False

        debug("inserting %s into node: %s" % (val, node))

        node.keys.append(val)
        node.keys.sort()
        
        if len(node.keys) > self.threshold:
            # overflow
            debug("  overflowing")
            self.overflow(node)
        else:
            # no overflow
            debug("  normal insert")

        return True


    def pretty(self):
        """ Given a tree, prettys it """

        def printNode(n, inc=1):
            print "%s%s (parent = %s)" % (" "*inc, n, n.parent)
            for c in n.children:
                printNode(c, inc+1)

        # print the tree structure

        print
        print "-start-"

        printNode(self.root)

        # get the left-most node

        node = self.root
        while node.children:
            node = node.children[0]

        # print the linked-list structure

        nodes = [node]
        while node.nextNode:
            node = node.nextNode
            nodes.append(node)

        print
        print " -> ".join([str(n) for n in nodes])

        # get the right-most node

        node = self.root
        while node.children:
            node = node.children[-1]

        # print the linked list structure

        nodes = [node]
        while node.prevNode:
            node = node.prevNode
            nodes.append(node)

        print
        print " -> ".join([str(n) for n in nodes])

        print
        print "-end-"


            
if __name__ == "__main__":

    t = Tree()

    basicSet = [1, 4, 5, 2, 3]
    advancedSet = [50, 100, 75, 200, 300, 400, 500, 40, 45, 55]
    megaSet = advancedSet + [600, 700, 800, 900, 1000, 1100, 1200, 1300]

    testSet = advancedSet

    if len(sys.argv) > 1:
        testSet = [ int(n) for n in sys.argv[1:]]

    for n in testSet:
        t.insert(n)
        t.pretty()



