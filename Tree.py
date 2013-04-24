#!/urs/bin/python
# Tested with python 2.7
## This is used to genorate the lookup object used by the other files.


class Node(object):

    node_count = 0

    def __init__(self):
        self.id = 0
        Node.node_count += 1
        self.leaf = False
        self.edges = {}

    def __str__(self):
        out = []
        if self.leaf:
            out.append("1")
        else:
            out.append("0")

        for label,node in self.edges.iteritems():
            out.append(label)
            out.append( str(node.id))

        return "_".join(out)


class DAWG(object):

    def __init__(self):
        self.prev = ""
        self.root = Node()

        self.unchecked_nodes = [] # List of tuple of the form (node,letter,next_node)
        self.checked_nodes   = {}

    def insert(self,string):
        if string < self.prev:
            raise ValueError, "Words not in alphabetical order - insert failed"

        prefix_length = 0
        for i in xrange(min (len(string),len(self.prev)  )):
            if string[i] != self.prev[i]:
                break
            prefix_length += 1


        self.compress(prefix_length)

        if len(self.unchecked_nodes) == 0:
            node = self.root
        else:
            node = self.unchecked_nodes[-1][2]

        for letter in word[prefix_length:]:
            next = Node()
            node.edges[letter] = next
            self.unchecked_nodes.append( (node,letter,next))
            node = next

        node.leaf = True
        self.prev = word

    def compress(self, downTo):
        for i in xrange(len(self.unchecked_nodes) - 1, downTo -1, -1):
            parent, letter, child = self.unchecked_nodes[i]

            if child in self.checked_nodes:
                parent.edges[letter] = self.checked_nodes[child]
            else:
                self.checked_nodes[child] = child
            self.unchecked_nodes.pop()

    def finish(self):
        self.compress(0)

    def lookup(self,string):
        node = self.root
        for letter in word:
            if letter not in node.edges:
                return False
            else:
                node = node.edges[letter]

        return node.leaf


if __name__ == '__main__':
    import sys
    import time

    DICTIONARY = "./wlist_match4"
    QUERY = ["derp",'the','true','aadfs','ooooo0oooooooooooooooo']
    #QUERY = ['000000000000']

    dawg = DAWG()
    WordCount = 0
    words = open(DICTIONARY, "rt").read().split()
    words.sort()
    start = time.time()    
    for word in words:
        WordCount += 1
        dawg.insert(word)
        if ( WordCount % 20000 ) == 0: print "%dr" % WordCount,
    dawg.finish()
    print "Dawg creation took %g s" % (time.time()-start)    


    for word in QUERY:
        if not dawg.lookup( word ):
            print "%s not in dictionary." % word
        else:
            print "%s is in the dictionary." % word


