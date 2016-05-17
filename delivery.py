class Delivery: 
    
    def __init__(self): 
        
        #placeholder values
        self.app_name = "APP"
        self.order_details = {
            "name": "Vincent",
            "item": "Toothbrush",
            "address": "44 HELLO STREET",
            "phone": 123456889
        }
        
        # keeps track of the user's state in the delivery process
        self.state = "INITIAL"
        
        self.quitting = False
        
        self.initial_prompt = ('You have ordered %s with %s.\n'
            'Do you recognize this purchase?') % (self.order_details['name'], self.app_name)    
    
    def process_input(self, input): 
        #TODO: handle error checking if wrong value 
        
        input = input.lower()
        response = ""
        
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
        if input == "yes":
            response = ('Thank you! \n'
                'Please confirm the following delivery information:\n'
                '\tNAME: %s\n'
                '\tADDRESS: %s\n'
                '\tCONTACT: %s\n'
                '\tITEM: %s'
                ) % (self.order_details['name'], self.order_details['address'], self.order_details['phone'], self.order_details['item'])
        elif input == "no":
            response = 'Thank you for your notification. We will cancel the order.'
            self.quitting = True
        return response 
            
    def confirmation(self, input): 
        if input == "yes":
            self.state = "ORDER_PLACED"
            response = 'Wonderful! Please look forward to messages in the next few days regarding the progress of your order.'

        elif input == "no":
            self.state == "INITIAL_CORRECTION"
            response = ('Please respond with the proper information in the following format:\n'
                '\"FIELD:new_value\"')
        return response 

        
    