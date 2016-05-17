import cmd # for cmdloop 

class DeliveryShell(cmd.Cmd):
    APP_NAME = "Delivery Shell"; 
    ITEM = "hat";
    
    intro = """
        Welcome to %s! You have ordered %s with our service.
        Do you recognize this purchase?
        """ % (APP_NAME, ITEM)
    
    promtp = "> order"
        
    def do_help(self, arg): 
        print "Help here."

if __name__ == '__main__':
    shell = DeliveryShell()
    shell.cmdloop()
    
