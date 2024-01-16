import sys
import pwinput
import paramiko
from paramiko_expect import SSHClientInteraction
import os
# Create variables for CUCM
print("*"*20 + "Enter credentials for UC system OS " + "*" *20)
CUCM_USERNAME=str(input("\033[1mUC OS username\033[0m, or press ENTER for default[admin]:").strip() or "admin")
CUCM_PASSWORD = pwinput.pwinput("\033[1mUC OS password: \033[0m")
if not CUCM_PASSWORD : print("Warning: Empty password entered")
CUCM_PORT="22"

print("*"*16 + " Enter command to execute on each servers " + "*" *16)
CUCM_CMD=str(input("\033[1mUC CMD\033[0m, or press ENTER for default[utils service restart Cisco CDP]:").strip() or "utils service restart Cisco CDP")

print("*"*16 + " Enter the file name with UC servers IP's " + "*" *16)
UCLIST_FILE=str(input("\033[1mCSV file with list of servers\033[0m, or press ENTER for default[ucservers-list.csv]:").strip() or "ucservers-list.csv")
if os.path.isfile(UCLIST_FILE):
   pass
else:  
    print(f"No such file: {UCLIST_FILE} in current directory")
    sys.exit()
sshsession = paramiko.SSHClient()
sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())     
with open(UCLIST_FILE) as file:
   
  for item in file:
   CUCM_ADDRESS = item.strip("\n") 
   print(CUCM_ADDRESS," <-connecting")
   try:
      sshsession.connect(hostname=CUCM_ADDRESS, username=CUCM_USERNAME, password=CUCM_PASSWORD, port=CUCM_PORT)
      # "display=True" is just to show you what script does in real time. While in production you can set it to False
      interact = SSHClientInteraction (sshsession, timeout=600, display=False)
      # program will wait till session is established and CUCM returns admin prompt
      interact.expect('admin:')
      # program runs command in CUCM OS
      interact.send(CUCM_CMD)
      # program waits for show status command to finish (this happen when CUCM returns admin prompt) 
      interact.expect('admin:')  
      cmd_output = interact.current_output_clean
      print(cmd_output)
   except paramiko.AuthenticationException as expc:
    print(f"Authentication Failed: {expc}")     
   except Exception as excp:
    print(f"Other error occurred: {excp}")
print ("*"*20 + " End " + "*" *20)