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

    def overflow(self, node):
        """ overflows a node """

        debug("overflowing")
        assert len(node.keys) > self.threshold

        keys = node.keys

        if not node.children:

            # is leaf

            debug ("  is leaf")

            if not node.parent:
                node.parent = Node(None)
                self.root = node.parent

            lnode = Node(node.parent)
            rnode = Node(node.parent)

            if node in node.parent.children:
                node.parent.children.remove(node)

            node.parent.children.append(lnode)
            node.parent.children.append(rnode)

            lnode.keys.append(keys[0])
            rnode.keys.append(keys[1])
            rnode.keys.append(keys[2])

            hoist = keys[1]
            node.parent.keys.append(hoist)

            if len(node.parent.keys) > self.threshold:
                self.overflow(node.parent)

        elif node == self.root:

            # I am root

            debug("  is root")

            # My keys will look like [A|B|C]

            newroot = Node(None)
            newroot.keys.append(keys[1])

            lnode = Node(node.parent)
            rnode = Node(node.parent)

            lnode.keys.append(keys[0])
            rnode.keys.append(keys[2])

            map(lnode.children.append, node.children[:2])
            map(rnode.children.append, node.children[2:])

            newroot.children.append(lnode)
            newroot.children.append(rnode)

            self.root = newroot

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

