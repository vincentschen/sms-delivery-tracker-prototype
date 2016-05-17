import time # for simulated waiting times
import datetime # for simulated delivery dates

class Delivery: 
    """This class is used in conjunction with the REPL class to handle all logic 
    between the user's inputs and the 'delivery process'. """
    
    def __init__(self): 
        """Initializes placeholder and state values for the Delivery prototype. """
        # PLACEHOLDER VALUES for delivery information
        self.app_name = "APP"
        self.courier = "Sneha"
        self.order_details = {
            "name": "Vincent",
            "item": "Toothbrush",
            "address": "44 HELLO STREET",
            "phone": 123456889
        }
        
        # STATE VARIABLES to keeps track of the delivery process
        self.state = "INITIAL"
        self.quitting = False
        
        # Initiate the messaging with this prompt 
        self.initial_prompt = ('You have ordered %s with %s.\n'
            'Do you recognize this purchase?') % (self.order_details['name'], self.app_name)    
    
    def process_input(self, input): 
        """ Handles all input in the REPL. """ 

        response = ""
        
        # make inputs case-insensitive 
        input = input.lower()
        
        if self.state == "INITIAL":
            response = self.initial(input)
            
        elif self.state == "CONFIRMATION":
            response = self.confirmation(input)
                    
        elif self.state == "INITIAL_CORRECTION":
            # TODO: parse initial correction field 
            response = "Thank you for the correction!"
            
        # elif self.state == "ORDER_PLACED":
            
        return response 
        
    def initial(self, input): 
        """ Handles possible responses for the INITIAL state """
        
        if input == "yes":
            
            # change state to confirmed 
            self.state = "CONFIRMATION"
            
            return ('Thank you! \n'
                'Please confirm the following delivery information:\n'
                '\tNAME: %s\n'
                '\tADDRESS: %s\n'
                '\tCONTACT: %s\n'
                '\tITEM: %s'
                ) % (self.order_details['name'], self.order_details['address'], self.order_details['phone'], self.order_details['item'])
        
        elif input == "no":
            
            # change 'quitting' flag, which will be detected in the REPL, quitting the prompt
            self.quitting = True
            return 'Thank you for your notification. We will cancel the order.'
        
        # input not recognized
        else: 
            return "Please respond with \'yes\' or \'no\' to confirm your order. Thank you!"
        
    def confirmation(self, input): 
        """ Handles possible responses for the CONFIRMATION state """

        if input == "yes":
            print 'Wonderful! Please look forward to messages in the next few days regarding the progress of your order.'
            
            # simulate "waiting" in real life
            for x in range(5): 
                print '.'
                time.sleep(1)
            
            self.state = "ORDER_PLACED"
            return self.order_placed()

        elif input == "no":
            #TODO: specify field in two steps 
            self.state == "INITIAL_CORRECTION"
            return ('Please respond with the proper information in the following format:\n'
                '\"FIELD:new_value\"')
                
    def order_placed(self):
        """ Handles possible responses for the ORDER_PLACED state """

        today = datetime.date.today()
        return ("Your delivery has been accepted by %s."
            "The expected date of delivery is %s.") % (self.courier, str(today))

        
    