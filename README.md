# Overview
This chat-based interface is a prototype for a delivery-tracking system. 

The command line functions as an SMS text interface -- where automated responses are incoming messages and user input are outbound messages.  

# Features 
This prototype tests the following user interactions: 
- denying incorrect orders 
- correcting incorrect delivery information 
- checking status while order is in transit or pending 
- contacting courier and recipient
- receiving updates after an uncertain amount of time
- handling failed deliveries
- providing overall feedback to courier service

Some user flows have been randomized to simulate a more realistic experience. 

Please run the prototype multiple times in order to experience different flows. 

# Install (OS X)
  1. Paste this link into your browser to download the `.zip` file.
https://github.com/vincentschen/sms-delivery-tracker-prototype/archive/master.zip

  2. Move the folder to your Desktop.
  
# Usage
  1. Open *Terminal*. You can do this by searching for "Terminal" in Spotlight. 
  2. Input: `cd ~/Desktop/sms-delivery-tracker-prototype`  
  3. Input: `python repl.py` 
  
Hit `CTRL + C` to force quit while the program is running.