from itertools import takewhile

is_tab = '\t'.__eq__

class Item:
    # Item for a given choice which keeps track of how it was accessed,
    # by which head gesture, how long the head gesture lasted, and lastly
    # uses a Watson API to formulate a response
    
    # private variables
    
    def __init__(self, gesture, choice):
        self.__parent = None        # previous choice item 
        self.__children = []        # next choice items
        self.gesture = gesture      # gesture - left, right, up, down head gestures
        self.choice = choice         # choice name (ex. order pizza, order drinks)
        self.data = []           # numerical data (for error checking)
        
    def add_child(self, child):
        self.__children.append(child)
        child.set_parent(self) #child.__parent = self
        
    def get_parent(self):
        return self.__parent
        
    def set_parent(self, parent):
        self.__parent = parent
        
    def get_child(self, ind):
        return self.__children[ind]

def build_tree(lines):
    # creates tree using an iterative inorder traversal approach
    
    lines = iter(lines)
    stack = []
    
    pdepth = 0                   # store prev depth
    
    tree = None                 # full tree from depth 0
    item = None                 # tree of current depth
    
    for line in lines:
        # get the depth by checking indents
        indent = len(list(takewhile(is_tab, line)))
    
        if indent == 0:
            # root node
            tree = Item("None", line.lstrip())
            item = tree
        else:
            if pdepth > indent:
                # done left branch, go back to root
                for i in range (0, (pdepth-indent)+1):
                    item = item.get_parent()
            elif pdepth == indent:
                # add a second child
                item = item.get_parent()
                
            l = line.lstrip().split(',')
            child = Item(l[0].lower(), l[1])
            item.add_child(child)
            
            # store backups
            item = child
            pdepth = indent
                
        stack[indent:] = [line.lstrip()]
        print "Adding path:" + str(stack)
    return tree

source = '''ROOT
\tChoice 1a
\t\tChoice 2a
\t\t\tChoice 3a
\t\t\tChoice 3b
\t\tChoice 2b
\t\t\tChoice 4a
\t\t\tChoice 4b
\tChoice 1b
\t\tChoice 5a
\t\t\tChoice 6a
\t\t\tChoice 6b
\t\tChoice 5b
\t\t\tChoice7a
\t\t\tChoice7b'''

with open("HT_system.txt", 'r') as f:
    data = f.read() 

tree = build_tree(data.split('\n'))
print(tree)