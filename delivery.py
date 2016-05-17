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
        
        self.initial_prompt = ('You have ordered %s with %s.\n'
            'Do you recognize this purchase?') % (self.order_details['name'], self.app_name)    
    
    def process_input(self, input): 
        input = input.lower()
        
        response = ""
        if self.state == "INITIAL":
            if input == "yes":
                self.state = "CONFIRMATION"
                response = ('Thank you! \n'
                    'Please confirm the following delivery information:\n'
                    '\tNAME: %s\n'
                    '\tADDRESS: %s\n'
                    '\tCONTACT: %s\n'
                    '\tITEM: %s\n'
                    )
            elif input == "no": 
                response = ('Please respond with the proper information in the following format:'
                    'FIELD: new_value')
                
        
        return response 
        
    