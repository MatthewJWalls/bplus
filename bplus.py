#!/usr/bin/env python

debugMode = False

def debug(s):
    if debugMode:
        print s

class Node:

    def __init__(self, parent=None):
        self.parent   = parent
        self.children = []
        self.keys     = []

    def __str__(self):
        return "node:<%s>" % self.keys

class Tree:
    
    def __init__(self):
        self.root = Node()
        self.threshold = 2 # this is hard coded for now

    def split(self, node, val):
        """ given a (leaf) node and a value, splits node 
        in order to add value to it """

        assert len(node.keys) == self.threshold

        keys = node.keys
        keys.append(val)
        keys.sort()

        # split this node into two other nodes (l and r)

        lnode = Node(node)
        rnode = Node(node)

        lnode.keys.append(keys[0])
        rnode.keys.append(keys[1])
        rnode.keys.append(keys[2])

        node.children.append(lnode)
        node.children.append(rnode)

        if node.parent is not None:
            node.parent.children.remove(node)
            lnode.parent = node.parent
            rnode.parent = node.parent
            node.parent.children.append(lnode)
            node.parent.children.append(rnode)
            debug("parent now has %d children" % len(node.parent.children))

        # put the hoist into the parent
        
        hoist = keys[1]

        if node.parent is None:
            # root node
            debug("As we are splitting the root, the hoist is erasing keys to [%s]" % hoist)
            node.keys = [hoist]
        else:
            # non root node
            debug("As we are NOT splitting the root, the hoist %s is being added to parent %s" % (hoist, node.parent))
            if len(node.parent.keys) == self.threshold:
                self.split(node.parent, hoist)
            else:
                node.parent.keys.append(hoist)

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

        debug("inserting %s into node: %s" % (val, node))
        
        if len(node.keys) == self.threshold:
            # split node
            debug("  splitting insert")
            self.split(node, val)
        else:
            debug("  normal insert")
            node.keys.append(val)
            node.keys.sort()

        return True


    def inspect(self):
        """ Given a tree, inspects it """

        def chiddlers(n, inc=1):
            print "%s%s" % (" "*inc, n)
            for c in n.children:
                chiddlers(c, inc+1)

        print
        print "-start-"
        chiddlers(self.root)
        print "-end-"

if __name__ == "__main__":

    t = Tree()

    # basic 

    assert t.insert(50)
    t.inspect()
    assert t.insert(100)
    t.inspect()
    assert t.insert(75)
    t.inspect()
    assert not t.insert(75)

    assert t.root.children[0].keys[0] == 50
    assert t.root.children[1].keys[0] == 75
    assert t.root.children[1].keys[1] == 100
    assert t.root.keys[0] == 75

    # now add another value and check the hoist

    t.insert(200)
    t.inspect()

    assert len(t.root.keys) == 2
    assert t.root.keys[0] == 75
    assert t.root.keys[1] == 100

    assert len(t.root.children) == 3
    assert len(t.root.keys) == 2
    assert t.root.children[0].keys[0] == 50
    assert t.root.children[1].keys[0] == 75
    assert t.root.children[2].keys[0] == 100
    assert t.root.children[2].keys[1] == 200

    debugMode = True
    t.insert(300)
    t.inspect()

