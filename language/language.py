#
# Language constants
#

WELCOME = "   Welcome to arpspoofKicker!"


#
# Universal
#

SELECT_AN_OPTION = "Select an option"


#
# main
#

MENU = "\n1. ARPSpoof a single device\n" \
       "2. ARPSpoof a multiple devices\n" \
       "E. Exit"

MENU_1 = "\n1. ARPSpoof a single device\n" \
         "2. ARPSpoof a multiple devices\n" \
         "3. Run thread(s) in queue\n" \
         "4. Stop running thread(s)\n" \
         "5. Print thread(s) status\n" \
         "E. Stop all threads and exit"


#
# Thread manager
#

THREAD_ENDED_UNEXPECTEDLY = "Thread %a ended unexpectedly"
NO_INTERFACES_WERE_FOUND = "No interfaces were found, check your network configuration, press enter to exit "
FOR_ARPSPOOF_CHECK_THIS = "To install 'arpspoof' check %a"
UPDATE_CONNECTED_USERS = "Re-scan"
THREAD_IS_NOT_RUNNING = "Thread %a is not running"
SELECT_AN_INTERFACE = "Select your network interface"
DISCOVERING_DEVICES = "\nRunning arp -a [Discovering devices]..."
SELECT_THE_GATEWAY = "Select a GATEWAY [Host]"
CONFIRM_INTERFACE = "Is %a your currently network interface?\n1. Yes\n2. No"
THREAD_IS_RUNNING = "Thread %a is running"
DUPLICATED_VICTIM = "A thread is already targeting %a"
SELECT_A_VICTIM = "Select a victim"
THREAD_CREATED = "A thread was created successfully"
SELECT_OPTIONS = "Select an option [ Selected %a of %a ]"
DELETE_THREAD = "Do you want delete thread %a?\n1. Yes\n2. No\n3. Stop/delete all"
STOP_THREAD = "Do you want stop thread %a?\n1. Yes\n2. No\n3. Stop/delete all"
VIEW_AS_MAC = "View as MAC address"
VIEW_AS_IP = "View as IPv4 address"
THREAD_V_G = " thread for victim %a and gateway %a"
STARTING = "Starting"
STOPPING = "Stopping"
DELETING = "Deleting"


#
# Util
#

IPCONFIG_COMMAND_NOT_FOUND = "ip or ifconfig command not found"
ARPSPOOF_PERMISSION_DENIED = "You need root permissions to run 'arpspoof'\n         Run with: sudo python3 main.py"
ARPSPOOF_COMMAND_NOT_FOUND = "'arpspoof' is not installed"
OPTION_IS_NOT_IN_LIST = "Your option is not in list, try any of these %a"
ARP_COMMAND_NOT_FOUND = "Somehow 'arp' command were not found (Likely you're using linux, install net-tools)"
STOPPING_ARPSPOOF = "Stopping arpspoof..."
INCOMPLETE_DATA = "Some devices were not detected as incomplete, consider re-scan for devices"
SELECT_ALL = "Select all"
FINISH = "Finish"
