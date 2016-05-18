import time # for simulated waiting times
import datetime # for simulated delivery dates
import random # to simulate 'chance' in delivery times and conditions
import sched # to schedule steate changes (simulating times in which we are waiting)
import threading # to run scheduling concurrently
import sys #for printing on same line #HACK

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
        self.app_name = "APP"
        self.courier = {
            'name': 'Sneha',
            'phone': 192857159
        }
        self.order_details = {
            "name": "Vincent",
            "item": "Toothbrush",
            "address": "44 HELLO STREET",
            "phone": 123456889
        }
        self.delivery_date = None
        
        # STATE VARIABLES to keeps track of the delivery process
        self.state = "INITIAL"
        self.quitting = False
        self.order_detail_to_change = None # set to value when user requesting change
        self.is_wating = False # boolean to indicate if currently waiting for state change

        # instance of scheduler 
        self.sched = sched.scheduler(time.time, time.sleep)
        
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
            response = self.initial_correction(input)
            
        elif self.state == "INITIAL_CORRECTION_CONFIRMED":
            response = self.initial_correction_confirmed(input)
            
        elif self.state == "ORDER_PLACED":
            
            if self.is_waiting:
                response = ("Our apologies! Your package has not been assigned just yet. "
                    "You will be notified shortly about any updates.")         
                
            else: 
                response = self.order_placed()
                    
        elif self.state == "ORDER_ACCEPTED":  
                          
            if self.is_waiting: 
                response = ("The status of your package has not been updated yet! "
                    "We will notify you when we have any new information.")
            
            else: 
                response = self.order_accepted()
                
        elif self.state == "ORDER_PENDING":
            self.schedulerThread.join()
            return self.order_pending()
            
        elif self.state == "ORDER_FAILED_FIXED":
            return self.order_failed_fixed()
                
        return response 
        
    def initial(self, input): 
        """ Handles possible responses for the INITIAL state """
        
        # change state to confirmed 
        self.state = "CONFIRMATION"
        
        if input == "yes":
            return ('Thank you! \n'
                'Please confirm the following delivery information:\n'
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

        if input == "yes" or input == "correct":
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
        self.order_details[self.order_detail_to_change] = input
        
        print "Great! The \'%s\' field has been changed to \'%s\'." % ( self.order_detail_to_change, input) 
        return self.order_placed()

    def order_placed(self): 
        """ Indicate an order has been properly placed into the system. """ 
        
        self.state = "ORDER_PLACED"

        # simulate time it takes for someone to claim the package for delivery
        seconds_to_state_change = 3 * random.randint(3, 5)
        self.schedule_state_change(seconds_to_state_change, "ORDER_ACCEPTED")

        return ('Wonderful! Please look forward to messages in the next few days regarding the progress of your order.'
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
        
    def get_random_later_date(self, curr_date):
        """ Generate delivery date within 1 to 5 days from current date randomly """

        num_days_later = random.randint(1, 5)
        return curr_date + datetime.timedelta(days=num_days_later)
        
    def order_pending(self): 
                
        # simulate failed delivery 30% of the time
        # if random.random() < 0.3:
            # order 'failed'
                    
            # simulate time it takes for delivery to be corrected
            seconds_to_state_change = 3 * random.randint(3, 5)
            self.schedule_state_change(seconds_to_state_change, "ORDER_FAILED_FIXED")
            
            self.delivery_date = self.get_random_later_date(self.delivery_date)
            return ("Unfortunately, there are issues with your delivery. "
                "%s noticed that your package was damaged, so we have stopped the delivery process.\n"
                "Your package will be delayed until %s. Please call this number if you have any questions: %s"
                ) % (self.courier['name'], str(self.delivery_date), str(self.courier['phone']))
        
        # else: 
        #     return "succes"
            
    def order_failed_fixed(self): 
        return ("We have corrected the delivery issue with your package. "
            "Please expect a a delivery on %s.") % str(self.delivery_date)
        
    def schedule_state_change(self, delay_in_seconds, new_state): 
        self.is_waiting = True
        self.sched.enter(5, 1, self.change_state, (new_state,))
        
        # spawn a thread to run in background
        self.schedulerThread = threading.Thread(target=self.sched.run) #TODO: currently no call to join
        self.schedulerThread.start()
        
    def change_state(self, new_state):
        self.is_waiting = False
        self.state = new_state
        sys.stdout.write("Delivery updated!\n> ") #HACK: prompts input, but not actually in REPL
        sys.stdout.flush() #use stdout for same line in HACK