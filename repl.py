import cmd # for REPL loop framework 
from delivery import *
from vendor.termcolor import colored # ref: https://pypi.python.org/pypi/termcolor

class REPL(cmd.Cmd):
    """Simple read, evaluate, print loop that uses imported Delivery class. to process information."""
    delivery = Delivery()
    prompt = "\n> "
    
    def preloop(self): 
        print '\n> ' + colored(self.delivery.initial_prompt, 'red')

    def default(self, line): 
        response = self.delivery.process_input(line)
        print '> ' + colored(response, 'red')
        
        if self.delivery.quitting:
            return True 

if __name__ == '__main__':
    repl = REPL()
    repl.cmdloop() 