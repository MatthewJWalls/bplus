#!/usr/bin/env python

class Node:

    def __init__(self):
        self.children = []
        self.keys = []
        self.isLeaf = True

class Tree:
    
    def __init__(self):
        self.root = Node()
        self.threshold = 2 # this is hard coded for now

    def split(self, node, val):
        """ given a (leaf) node and a value, splits node 
        in order to add value to it """

        assert node.isLeaf
        assert len(node.children) == 0
        assert len(node.keys) == self.threshold

        keys = node.keys
        keys.append(val)
        keys.sort()

        # push keys out into children

        lnode = Node()
        rnode = Node()

        lnode.keys.append(keys[0])
        rnode.keys.append(keys[1])
        rnode.keys.append(keys[2])

        node.children.append(lnode)
        node.children.append(rnode)

        # hoist a splitter up into the node

        node.keys = [keys[1]]

        # node is no longer a leaf

        node.isLeaf = False

    def find(self, val, node=None):

        # recurse down the right tree path until we hit the
        # leaf node that the value should be in, then return
        # a tuple, t where t[0] is True or False depending on
        # whether the value was found, and t[1] is the leaf
        # node where the value _should_ have been.

        if node is None:
            node = self.root

        print "inspecting a node"

        if node.children:

            # non-leaf, we need to work out what child to
            # descend to, and then recurse

            print "  Not a leaf"

            nodeToDescend = 0

            for i, k in enumerate(node.keys):
                print "  %d < %d?" % (val, k)
                if val < k:
                    print "    yes"
                    break
                else:
                    nodeToDescend += 1
                    print "    no"

            if nodeToDescend is None:
                nodeToDescend 

            print "  Descending to a child node %d" % nodeToDescend
            return self.find(val, node.children[nodeToDescend])
                    
        else:

            # leaf

            print "  Leaf"

            if val in node.keys:
                print "  Found", val, "in the tree"
                return (True, node)
            else:
                # it's not in the tree
                print "  ", val, "was not in the tree"
                return (False, node)

    def insert(self, val):

        print "inserting %s" % val

        #found, node = self.find(sval)
        
        if len(self.root.keys) == self.threshold:
            # split root
            print "splitting"
            self.split(self.root, val)
        else:
            self.root.keys.append(val)


def inspectTree(t):
    """ Given a tree, inspects it """

    print "root:"
    print "  children: %d" % len(t.root.children)
    print "  keys: %s" % t.root.keys

if __name__ == "__main__":

    t = Tree()
    t.insert(50)
    t.insert(100)
    t.insert(75)

    inspectTree(t)

    print
    t.find(t.root, 50)
    print
    t.find(t.root, 100)
    print
    t.find(t.root, 75)
    print
    t.find(t.root, 90)

