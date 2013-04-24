#!/urs/bin/python
# Tested with python 2.7
## This is used to genorate the lookup object used by the other files.


class Node(object):

    node_count = 0

    def __init__(self):
        self.id = 0 ## Each node in a tree is represented by a unique integer id
        Node.node_count += 1 ## We keep track of how many nodes there are using this
        self.leaf = False ## Leaf is False if a node has a child, True otherwise
        self.edges = {} ## edges[nex_letter] = node associated with letter

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
        self.prev = ""  ## The previous node in the tree. Empty for root
        self.root = Node() ## The root node of the tree

        self.unchecked_nodes = [] # List of tuple of the form (node,letter,next_node).
                                  # Can contain duplicates
        self.checked_nodes   = {} 

    def insert(self,string):
        ''' Inserts strings into the tree. Strings must be inserted in alphabetical order '''
        if string < self.prev:
            raise ValueError, "Words not in alphabetical order - insert failed"

        ## The number of letters shared between keys. For example, ant and and would have a
        ## prefix_length of 2
        prefix_length = 0
        for i in xrange(min (len(string),len(self.prev)  )): ## Incriments prefix_length for each letter
            if string[i] != self.prev[i]:                    ## which is the same
                break
            prefix_length += 1


        self.compress(prefix_length)

        if len(self.unchecked_nodes) == 0:
            node = self.root
        else:
            node = self.unchecked_nodes[-1][2] ## The second position contains a node object

        ## Traverses down the tree, putting the word in the correct spot
        for letter in word[prefix_length:]:
            next = Node()
            node.edges[letter] = next
            self.unchecked_nodes.append( (node,letter,next))
            node = next

        ## When it's reached the bottom of the tree, we must be at a leaf
        node.leaf = True
        self.prev = word

    def compress(self, downTo):

        ## Merge each unchecked node into other (checked) nodes with the same prefixes
        for i in xrange(len(self.unchecked_nodes) - 1, downTo -1, -1):
            parent, letter, child = self.unchecked_nodes[i]

            if child in self.checked_nodes:
                parent.edges[letter] = self.checked_nodes[child]
            else:
                self.checked_nodes[child] = child
            self.unchecked_nodes.pop()

    def finish(self):
        ''' Call this when you've added the last word '''
        self.compress(0)

    def lookup(self,string):
        ''' string -> bool, returns True if the tree contains a string, False otherwise'''
        node = self.root
        for letter in word:
            if letter not in node.edges:
                return False
            else:
                node = node.edges[letter]

        return node.leaf

def make_tree(path_to_wordlist):
    '''
    NOT IMPLIMENTED
    makes a tree given the filename of a dictionary. Basically does what the main block does now.
    '''

    pass
    
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
<<<<<<< HEAD


# I am the uber awesome supreme RULER of the bitspace - Ahrar
=======
>>>>>>> 9f37e202070b1fc979aa39fbadb5365883da4cf1
