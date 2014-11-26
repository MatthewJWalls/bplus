#!/usr/bin/env python

class Node:

    def __init__(self, parent=None):
        self.parent   = parent
        self.children = []
        self.keys     = []
        self.isLeaf   = True

    def __str__(self):
        return "node:<%s>" % self.keys

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

        lnode = Node(node)
        rnode = Node(node)

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
                return (True, node)
            else:
                # it's not in the tree
                return (False, node)

    def insert(self, val):

        found, node = self.find(val)
        assert node is not None

        if found:
            return False
        
        if len(node.keys) == self.threshold:
            # split node
            self.split(node, val)
        else:
            node.keys.append(val)
            node.keys.sort()

        return True


def inspectTree(t):
    """ Given a tree, inspects it """

    def chiddlers(n, inc=1):
        print "%s%s" % (" "*inc, n)
        for c in n.children:
            chiddlers(c, inc+1)

    chiddlers(t.root)

if __name__ == "__main__":

    t = Tree()

    # basic 

    assert t.insert(50)
    assert t.insert(100)
    assert t.insert(75)
    assert not t.insert(75)

    assert t.root.children[0].keys[0] == 50
    assert t.root.children[1].keys[0] == 75
    assert t.root.children[1].keys[1] == 100
    assert t.root.keys[0] == 75

    # now add another value and check the hoist
    
    t.insert(200)
    assert len(t.root.keys) == 2
    assert t.root.keys[0] == 75
    assert t.root.keys[1] == 100

    assert len(t.root.children) == 3
    assert len(t.root.keys) == 2
    assert t.root.children[0].keys[0] == 50
    assert t.root.children[1].keys[0] == 75
    assert t.root.children[2].keys[0] == 100
    assert t.root.children[2].keys[1] == 200

    print
    inspectTree(t)

