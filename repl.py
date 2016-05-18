import cmd # for REPL loop framework 
from delivery import *

class REPL(cmd.Cmd):
    """Simple read, evaluate, print loop that uses imported Delivery class. to process information."""
    delivery = Delivery()
    prompt = "\n> "
    
    def preloop(self): 
        print '\n', self.delivery.initial_prompt

    def default(self, line): 
        response = self.delivery.process_input(line)
        print response 
        
        if self.delivery.quitting:
            return True 
            
if __name__ == '__main__':
    repl = REPL()
    repl.cmdloop() 