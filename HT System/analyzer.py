from pymongo import MongoClient
from itertools import takewhile
from utils import *

is_tab = '\t'.__eq__

class HTSystem:
    # Head tracking system which consists of an infrustructure of items
    # which can be traversed through head tilts
    
    def __init__(self, f_name="HT_system.txt"):
        '''
        input: 
        p_name - participant's name (Client)
        sys - nested array of options in the form []
        output: none
        '''
        self.record = False       # when true, begin recording information        
        self.load_sys()           # load system information from file
    
    def load_sys(self, f_name):
        '''
        Loads the file containing system information
        input:
        f_name = file name
        '''
        with open(self.__fname, 'r') as f:
            self.__fdata = f.read() 
            
        self.build_tree(data.split('\n'))
    
    def build_tree(self, data):
        # creates tree using an iterative inorder traversal approach
        
        data = iter(data)
        stack = []
        
        pdepth = 0                   # store prev depth
        
        self.__tree = None          # full tree from depth 0
        item = None                 # tree of current depth
        
        for line in data:
            # get the depth by checking indents
            indent = len(list(takewhile(is_tab, line)))
        
            if indent == 0:
                # root node
                self.__tree = Item("None", line.lstrip())
                item = self.__tree
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
            
        # set the current active node as the tree
        self.__curr = self.__tree  
            
    def add_client(self, fname, lname):
        client = Client(fname, lname)
        self.set_client(client)
        
    def set_client(self, client):
        self.client = client
        
    def save(self):
        ''' Saves the data to mongodb and saves the drawn graph '''
        # go through all items and save them
        
class Client:
    # The participants information in case we need to store it in the 
    # database as well
    
    def init(self, fname, lname):
        self.__fname = fname
        self.__lname = lname
        # place any other information we might want stored in the db here
        
    def set_fname(self, name):
        self.__fname = name
        
    def set_lname(self, name):
        self.__lname = name    
        
    def get_fname(self):
        return self.__fname
        
    def get_lname(self):
        return self.__lname

    def get_fullname(self):
        return self.get_fname + " " + self.get_lname
        
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
        
    def draw(self):
        # draws the graph for the corresponding data
        return
        
    def save(self):
        # saves the data
        return
    
    def speak(self):
        length = len(self.__children)
        text = ""
        
        if length > 2:
            for i in range (0, length):
                text += self.__children[i].gesture + " to select choice " + \
                    self.__children[i].choice
    

        
if __main__ == "__name__":
    system = HTSystem()