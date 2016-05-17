class Delivery: 
    
    def __init__(self): 
        
        #placeholder values
        self.app_name = "APP"
        self.order_details = {
            "name": "NAME",
            "item": "ITEM",
            "address": "44 HELLO STREET",
            "phone": 123456889
        }
        
        # keeps track of the user's state in the delivery process
        self.state = "INITIAL"
        
        self.quitting = False
        
        self.initial_prompt = ('You have ordered %s with %s.\n'
            'Do you recognize this purchase?') % (self.order_details['name'], self.app_name)    
    
    def process_input(self, input): 
        input = input.lower()
        response = ""
        
        if self.state == "INITIAL":
            if input == "yes":
                response = ('Thank you! \n'
                    'Please confirm the following delivery information:\n'
                    '\tNAME: %s\n'
                    '\tADDRESS: %s\n'
                    '\tCONTACT: %s\n'
                    '\tITEM: %s\n'
                    )
            elif input == "no":
                response = 'Thank you for your notification. We will cancel the order.'
                self.quitting = True
            
        elif self.state == "CONFIRMATION":
            if input == "yes":
                self.state = "PENDING"

            elif input == "no":
                self.state == "INITIAL_CORRECTION"
                response = ('Please respond with the proper information in the following format:\n'
                    '\"FIELD:new_value\"')
                    
        elif self.state == "INITIAL_CORRECTION":
            # TODO: parse initial correction field 
            response = "Thank you for the correction!"
                
        return response 
        
    