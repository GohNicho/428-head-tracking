from itertools import takewhile
from utils import *
from db import *
import time

is_tab = '\t'.__eq__

class Client:
    # The participants information in case we need to store it in the 
    # database as well
    
    def __init__(self, fname, lname):
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
    
    def get_info(self):
        # returns all info in an array of tuples
        return [("first_name",self.get_fname()), ("last_name",self.get_lname())]
        
class Item:
    # Item for a given choice which keeps track of how it was accessed,
    # by which head gesture, how long the head gesture lasted, and lastly
    # uses a Watson API to formulate a response
    
    # private variables
    
    def __init__(self, gesture, choice):
        self.__parent = None        # previous choice item 
        self.__children = []        # next choice items
        self.gesture = gesture      # gesture - left, right, up, down head gestures
        self.choice = choice        # choice name (ex. order pizza, order drinks)
        self.time = 0               # how long the gesture lasted
        self.picked = False         # whether this choice was picked
        
    def set_picked(self):
        self.picked = True
        
    def was_picked(self):
        return self.picked
        
    def has_children(self):
        return True if self.__children else False
    
    def num_children(self):
        return len(self.__children)
        
    def select_choice(self, t, gesture):
        '''
        Given a gesture, returns the next choice
        '''
        
        # save the time of the transaction
        self.time = time.time()-t
        
        for child in self.__children:
            if child.get_gesture() == gesture:
                child.set_picked()
                return (child.get_choice(), self.time, child)
        
    def add_child(self, child):
        self.__children.append(child)
        child.set_parent(self)
        
    def get_parent(self):
        return self.__parent
        
    def set_parent(self, parent):
        self.__parent = parent
        
    def get_child(self, ind):
        return self.__children[ind]
    
    def get_gesture(self):
        return self.gesture
    
    def get_choice(self):
        return self.choice
    
    def get_time(self):
        return self.time
        
    def draw(self):
        # draws the graph for the corresponding data
        return
    
    def speak(self):
        '''
        generate the text that will be spoken out loud by an api
        '''
        
        # speak the decision here
        if not self.has_children():
            print ("You've selected " + self.choice)
        
        # NTS: maybe add a wait time here
        
        length = len(self.__children)
        text = ""
        
        # remake text rather than storing in case the choices are changed
        if length >= 2:    
            for i in range (0, length):
                text += "Rotate your head to the " + self.__children[i].gesture \
                    + " to select choice " + self.__children[i].choice + \
                    (", " if i < length-1 else ".")
        elif self.has_children():
            text = self.__children[-1].choice
            
        # CALL TEXT TO SPEECH API HERE
        print (text)
        
        return True

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
        self.__fname = f_name
        self.load_sys()           # load system information from file
        self.__data = []          # numerical data (for error checking)
        self.__db = Database()    # load up the database for the system
        self.__incomp_gest = False  # True if waiting for a gesture to be completed
        self.__progress = "none"        # Intermediate var-determine full head gesture
        self.__start = time.time()
        self.saved = False              # Check whether we saved the client info
        self.client = Client("Test", "Test")
        self.times = []                 # Store the times since we changed to state machine
        
        if (self.__curr.speak()):
            # Begin tracking
            self.start_timer()
    
    def start_timer(self):
        self.__start = time.time()    
    
    def load_sys(self):
        '''
        Loads the file containing system information
        input:
        f_name = file name
        '''
        with open(self.__fname, 'r') as f:
            self.__fdata = f.read() 
            
        self.build_tree(self.__fdata.split('\n'))
    
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
                child = Item(l[0].lower(), "".join(l[1:]))
                item.add_child(child)
                
                # store backups
                item = child
                pdepth = indent
                    
            stack[indent:] = [line.lstrip()]
            print ("Adding path:" + str(stack))
            
        # set the current active node as the tree
        self.__curr = self.__tree  
            
    def add_client(self, fname, lname):
        client = Client(fname, lname)
        self.set_client(client)
        
    def set_client(self, client):
        self.client = client
        
    def read(self, vals, gesture):
        '''
        reads the filtered values from the arduino and the gesture
        input:
        vals - an array of len 4 that contains
        gesture - type of gesture (left, right, top)
        '''

        # store the values
        self.__db.add_tracking(vals, gesture)
        
        # perform drawing code here
        
        # check if a gesture is occurring
        
        if self.__progress.lower() in ["left", "right", "up", "down"] and \
           gesture.lower() == "none":
            # an action has been performed
            print ("You've moved your head " + str(self.__progress.lower()))
            
            ch, ti, child = self.__curr.select_choice(self.__start, self.__progress)
            self.times.append((ch,ti))
            
            self.__curr = self.__tree
            
            # speak
            child.speak()
            print ("Press enter to continue, press q to stop the program")
            ch = input()           
            
            if ch.lower() == 'q':
                # quitting
                print ("Have a nice day!")
                self.save()    
                exit()
                
            # Begin tracking
            self.start_timer()             
        else:
            # gesture is none so we'll save it
            self.__progress = gesture.lower();

        
        
    def get_choices_tree(self):
        tree = self.__tree
        arr = []
        
        while tree.has_children():
            for i in range (0, tree.num_children()):
                if tree.get_child(i).was_picked():
                    # picked this, store it's info
                    arr.append((tree.get_choice(), tree.get_time()))
                    tree = tree.get_child(i)
                    break
        return arr
        
    def save(self):
        ''' Saves client information the drawn graph '''
        # go through all items and save them
        self.__db.add_client(self.client, self.times)
        self.saved = True
    

        
if __name__ == '__main__':
    system = HTSystem()
    system.add_client("Vera", "Sipicki")
    print ('done')