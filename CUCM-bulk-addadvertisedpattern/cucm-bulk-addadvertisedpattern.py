import requests
import urllib3
import zeep
from zeep import exceptions
import pwinput
import pandas
import os
import sys
# Create variables for CUCM host and credentials
print("*"*20 + " Enter IP, version and credentials for CUCM API " + "*" *20)
CUCM_ADDRESS=str(input("CUCM IP address:"))
if not CUCM_ADDRESS : print("Warning: Empty CUCM IP entered")
CUCM_VERSION=str(input("CUCM version[12.5]:").strip() or "12.5")
CUCM_USERNAME=str(input("API CUCM username[admin]:").strip() or "admin")
CUCM_PASSWORD = pwinput.pwinput()
if not CUCM_PASSWORD : print("Warning: Empty password entered")

# Create and verification variable for the CUCM 14 AXL WSDL File location 
AXL_WSDL_FILE = f"./axlsqltoolkit/schema/{CUCM_VERSION}/AXLAPI.wsdl"
if os.path.isfile(AXL_WSDL_FILE):
   pass
else:  
  print(f"No such WSDLfile: {AXL_WSDL_FILE} in current directory or incorrect CUCM ver. entered")
  sys.exit()

# Create and verification variable for source file name with data
print("*"*20 + " Enter CSV file with data located in current directory " + "*" *20)
SRC_FILE=str(input("Source CSV file name[srcfile.csv]:").strip() or "srcfile.csv")
if os.path.isfile(SRC_FILE):
   pass
else:  
    print(f"No such file: {SRC_FILE} in current directory")
    sys.exit()

CSV_DATA=pandas.read_csv(SRC_FILE)

# Create an instance of requests.Session that we will use with the zeep.Client
session = requests.Session()
# Disable SSL Certificate verification
session.verify = False
# Disable insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Configure session authentication with basic auth method using CUCM credentials
session.auth = requests.auth.HTTPBasicAuth(CUCM_USERNAME, CUCM_PASSWORD)
# Create an instance of zeep HistoryPlugin in order to debug the sent and received SOAP Payloads
history = zeep.plugins.HistoryPlugin()
# Create an instance of the zeep.Client using the axl_wsdl file
# and the session object as the transport and with the history plugin
client = zeep.Client(wsdl=AXL_WSDL_FILE, transport=zeep.Transport(session=session),
                     plugins=[history] )
# Create the AXL Service binding to your POD's CUCM AXL service URL
# Defaults to https://ccmservername:8443/axl/
service = client.create_service('{http://www.cisco.com/AXLAPIService/}AXLAPIBinding',
                                f'https://{CUCM_ADDRESS}:8443/axl/')

# Configuration patterns in loop
print ("*"*20 + " Configuring the CUCM " + "*" *20)
for ind in CSV_DATA.index:
   ADVERTISED_PATTERN = {
    'pattern': CSV_DATA['pattern'][ind],
    'description' : CSV_DATA['description'][ind]
    }
   print(ADVERTISED_PATTERN," <-adding")
   try:
      add_Advertised_Patterns = service.addAdvertisedPatterns(advertisedPatterns = ADVERTISED_PATTERN)
   except requests.RequestException as expc:
    print(f"REQUESTS module Fault: {expc}")
   except exceptions.Error  as expc:
    print(f"SOAP module Error: {expc} <- advice check CUCM IP and credentials")
   except exceptions.Fault  as expc:
    print(f"SOAP module Fault: {expc}")           
   except Exception as excp:
    print(f"Other error occurred: {excp}")

   #log outbound soap payload sent to CUCM AXL API  (uncomment it for debug)
   #print('\n %s', etree.tostring(history.last_sent["envelope"], encoding="unicode", pretty_print=True))
   # log inbound soap payload received from CUCM AXL API (uncomment it for debug)
   #print('\n %s', etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True))
   
print ("*"*20 + " End " + "*" *20)

