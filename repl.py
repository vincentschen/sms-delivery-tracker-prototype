import cmd # for REPL loop framework 
from delivery import *
from vendor.termcolor import colored # ref: https://pypi.python.org/pypi/termcolor

class REPL(cmd.Cmd):
    """Simple read, evaluate, print loop that uses imported Delivery class. to process information."""
    delivery = Delivery()
    prompt = "\n> "
    
    def preloop(self): 
        print_red('\n' + self.delivery.initial_prompt)

    def default(self, line): 
        response = self.delivery.process_input(line)
        print_red(response)
        
        if self.delivery.quitting:
            return True 

def print_red(text):
    print colored(text, 'red')

if __name__ == '__main__':
    repl = REPL()
    repl.cmdloop() 