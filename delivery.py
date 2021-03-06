import time # for simulated waiting times
import datetime # for simulated delivery dates
import random # to simulate 'chance' in delivery times and conditions
import sched # to schedule steate changes (simulating times in which we are waiting)
import threading # to run scheduling concurrently
import sys #for printing on same line #HACK
import re #for regex validation
from vendor.termcolor import colored

class Delivery: 
    """
    This class is used in conjunction with the REPL class to handle all logic 
    between the user's inputs and the 'delivery process'. 
    
    How it works: 
    After the input is processed, change the state so that the REPL can move forward. 
    
    """
    
    def __init__(self): 
        """Initializes placeholder and state values for the Delivery prototype. """
        # PLACEHOLDER VALUES for delivery information
        self.app_name = "DeliverSA"
        self.courier = {
            'name': 'Sneha',
            'phone': '+27 081 987 6543'
        }
        self.order_details = {
            "name": "Vincent",
            "item": "Lenovo Laptop",
            "address": "4 Main Road",
            "phone": '+27 081 123 4567'
        }
        self.delivery_date = None
        
        # STATE VARIABLES to keeps track of the delivery process
        self.state = "INITIAL"
        self.quitting = False
        self.order_detail_to_change = None # set to value when user requesting change
        self.is_waiting = False # boolean to indicate if currently waiting for state change

        # instance of scheduler 
        self.sched = sched.scheduler(time.time, time.sleep)
        
        # Initiate the messaging with this prompt 
        self.initial_prompt = ('You have ordered \"%s\" with %s.\n'
            'Do you recognize this purchase? [yes/no]') % (self.order_details['item'], self.app_name)    

        #DEBUG flag
        self.DEBUG = False
    
    def process_input(self, input): 
        """ Handles all input in the REPL. """ 

        if self.DEBUG:
            print colored(self.state, 'green')

        response = ""
        # make inputs case-insensitive 
        input = input.lower()
        
        if self.state == "INITIAL":
            response = self.initial(input)
            
        elif self.state == "CONFIRMATION":
            response = self.confirmation(input)
                    
        elif self.state == "INITIAL_CORRECTION":
            response = self.initial_correction(input)
            
        elif self.state == "INITIAL_CORRECTION_CONFIRMED":
            response = self.initial_correction_confirmed(input)
            
        elif self.state == "ORDER_PLACED":
            
            if self.is_waiting: # state has not changed yet
                response = ("Our apologies! Your package has not been assigned just yet. "
                    "Please check back shortly for updates!")         
                
            else: 
                response = self.order_placed()
                    
        elif self.state == "ORDER_ACCEPTED":  
                          
            if self.is_waiting: # state has not changed yet
                response = ("The status of your package has not been updated yet. "
                    "Please check back shortly for updates!")
            
            else: 
                response = self.order_accepted()
                
        elif self.state == "ORDER_PENDING":
            response = self.order_pending()
            # self.schedulerThread.join()
            
        elif self.state == "ORDER_FAILED_FIXED":
            response = self.order_failed_fixed()
                
        elif self.state == "ORDER_APPROACHING":
            if self.is_waiting: 
                response = ("Your package is in transit. "
                    "Please check back shortly for updates!")
            
            else: 
                response = self.order_approaching()
            
        elif self.state == "ORDER_ARRIVED":
            response = self.order_arrived()
            
        elif self.state == "ARRIVAL_CONFIRMATION":
            response = self.arrival_confirmation(input)
            
        elif self.state == "FEEDBACK":
            response = self.feedback(input)
            
        return response 
        
    def initial(self, input): 
        """ Handles possible responses for the INITIAL state """
        
        # change state to confirmed 
        self.state = "CONFIRMATION"
        
        if input == "yes":
            return ('Thank you! \n'
                'Is the following delivery information correct? [yes/no]\n'
                '\tNAME: %s\n'
                '\tADDRESS: %s\n'
                '\tPHONE: %s\n'
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

        if input == "yes" or input == "correct" or input == "confirm":
            return self.order_placed()

        elif input == "no" or input == "incorrect":
            self.state = "INITIAL_CORRECTION"
            return 'What field would you like to correct?'
            
        else: 
            return "Please response with \'correct\' or \'incorrect\' to confirm your delivery information."
                
    def initial_correction(self, input):
        
        # store dictionary keys in a set
        order_details_set = self.order_details.keys()
        
        if input in order_details_set: 
            self.order_detail_to_change = input
            self.state = "INITIAL_CORRECTION_CONFIRMED"
            return "Please enter the correct value for %s:" % input 
        
        # input is not one of the appropriate fields 
        else:
            response = "The input you selected is invalid. Please enter one of the following:" 
            
            # print each item in the list of order details
            for detail in order_details_set: 
                response += "\n\'%s\'" % detail
            return response 
                
    def initial_correction_confirmed(self, input): 
        if self.correction_is_valid(self.order_detail_to_change, input): 
            self.order_details[self.order_detail_to_change] = input
            
            self.state = "CONFIRMATION"
            return ("The \'%s\' field has been changed to \'%s\'.\n\n"
                'Is the following delivery information correct? [yes/no]\n'
                '\tNAME: %s\n'
                '\tADDRESS: %s\n'
                '\tPHONE: %s\n'
                '\tITEM: %s'
                ) % (self.order_detail_to_change, input, self.order_details['name'], self.order_details['address'], self.order_details['phone'], self.order_details['item'])

        else: 
            return "Your input format for the \"%s\" field is invalid. Please try again." % self.order_detail_to_change
            

    def order_placed(self): 
        """ Indicate an order has been properly placed into the system. """ 
        
        self.state = "ORDER_PLACED"

        # simulate time it takes for someone to claim the package for delivery
        seconds_to_state_change = 3 * random.randint(3, 5)
        self.schedule_state_change(seconds_to_state_change, "ORDER_ACCEPTED")

        return ('Please look forward to messages in the next few days regarding the progress of your order. '
            '[To check on status, please respond to this number with any text.]')
                
    def order_accepted(self):
        """ Handles possible responses for the ORDER_PLACED state """

        self.state = "ORDER_ACCEPTED"

        # simulate time it takes for someone to claim the package for delivery
        seconds_to_state_change = 3 * random.randint(3, 5)
        self.schedule_state_change(seconds_to_state_change, "ORDER_PENDING")

        self.delivery_date = self.get_random_later_date(datetime.date.today())
        
        return ("Your delivery has been accepted by %s. "
            "The expected date of delivery is %s.") % (self.courier['name'], str(self.delivery_date))
        
    def order_pending(self): 
                
        # simulate failed delivery 50% of the time for demo's sake
        if random.random() < 7.0: # order failed
            
            if not self.is_waiting: 
                # simulate time it takes for delivery to be corrected
                seconds_to_state_change = 3 * random.randint(3, 5)
                self.schedule_state_change(seconds_to_state_change, "ORDER_FAILED_FIXED")
            
                self.delivery_date = self.get_random_later_date(self.delivery_date)
                
            return ("Unfortunately, there are issues with your delivery. "
                "%s noticed that your package was damaged, so we have stopped the delivery process.\n"
                "Your package will be delayed until %s. Please call this number if you have any questions: %s"
                ) % (self.courier['name'], str(self.delivery_date), str(self.courier['phone']))
        
        else: # order succeeded
            return self.order_approaching()

    def order_failed_fixed(self): 
        if not self.is_waiting: 
            self.schedule_state_change(15, 'ORDER_APPROACHING')
        
        return ("We have corrected the delivery issue with your package. "
            "Please expect a a delivery on %s.") % str(self.delivery_date)

    def order_approaching(self):
        self.schedule_state_change(15, "ORDER_ARRIVED")
        
        minutes_to_arrival = random.randint(5, 30)
        return ("Your package will arrive in %s minutes. "
            "If there are any issues, expect a call from %s. "
            "Might you have any questions, feel free to phone this number: %s."
            ) % (str(minutes_to_arrival), self.courier['name'], self.courier['phone'])

    def order_arrived(self):
        
        self.state = "ARRIVAL_CONFIRMATION" #set next state
        
        return ("Your order has arrived. Please contact %s by phone: %s.\n"
        "Once your receive your package, please respond \'confirmed\'!"
        ) % (self.courier['name'], self.courier['phone'])

    def arrival_confirmation(self, input):
        if input == "confirmed":
            self.state = "FEEDBACK" #set next state 
            return ("Thank you for your patience! Please rate your experience 1 to 5.")
        else: 
            return ("Once your receive your package, please respond \'confirmed\'! "
                "If you have any issues, please call %s.") % self.courier['phone']

    def feedback(self, input):
        if not input.isdigit(): 
            #validation -- makes sure the input is only a number
            return "Please respond with a value between 1 and 5, inclusive!"
        
        possible_ratings = [1, 2, 3, 4, 5]
        if int(input) in possible_ratings: # validate rating input
            self.quitting = True 
            return ("We appreciate your feedback! We look forward to serving you next time.")
        else: 
            return "Please respond with a value between 1 and 5, inclusive!"

# UTILITY FUNCTIONS (for state management, time management)

    def schedule_state_change(self, delay_in_seconds, new_state): 
        self.is_waiting = True
        self.sched.enter(5, 1, self.change_state, (new_state,))
        
        # spawn a thread to run in background
        self.schedulerThread = threading.Thread(target=self.sched.run) #TODO: currently no call to join
        self.schedulerThread.start()
        
    def change_state(self, new_state):
        self.is_waiting = False
        self.state = new_state
        
        if self.DEBUG:
            print colored(self.state, 'green') #DEBUG
        
        text = ("Delivery updated!\n"
         "Please respond to this number with any text to view your status.\n") #HACK: prompts input, but not actually in REPL
        
        text = colored(text, 'red') + "\n> " 
        sys.stdout.write(text)
        sys.stdout.flush() #use stdout for same line in HACK
        
    def get_random_later_date(self, curr_date):
        """ Generate delivery date within 1 to 5 days from current date randomly """

        num_days_later = random.randint(1, 5)
        return curr_date + datetime.timedelta(days=num_days_later)
        
        
    def correction_is_valid(self, field, input):
        """ Performs simple checks to see if the input is valid."""
        
        if field == "name": 
            name_regex = r'[a-zA-Z \-]+'
            if re.match(name_regex, input): 
                return True
            else: 
                return False            
                
        elif field == "address":
            address_regex = r'\d+ [a-zA-Z \.\,]+'
            if re.match(address_regex, input): 
                return True
            else: 
                return False
            
        elif field == "phone":
            #checks if there is some digit 
            return any(char.isdigit() for char in input)
        
        else: 
            
            #accept any input for 'item'
            return True 
        