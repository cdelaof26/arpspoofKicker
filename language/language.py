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
MENU = "1. ARPSpoof a single device\n" \
       "2. ARPSpoof a multiple devices\n" \
       "E. Exit"

NO_INTERFACES_WERE_FOUND = "No interfaces were found, check your network configuration, cannot continue"
SELECT_AN_INTERFACE = "Select your network interface"
DISCOVERING_DEVICES = "\nRunning arp -a [Discovering devices]..."
VIEW_AS_MAC = "View as MAC address"
VIEW_AS_IP = "View as IPv4 address"
UPDATE_CONNECTED_USERS = "Re-scan"
FOR_ARPSPOOF_CHECK_THIS = "To install 'arpspoof' check %a"
SELECT_A_VICTIM = "Select a victim"
SELECT_THE_GATEWAY = "Select a gateway [Host]"


#
# Util
#
OPTION_IS_NOT_IN_LIST = "Your option is not in list, try any of these %a"
IPCONFIG_COMMAND_NOT_FOUND = "ip or ifconfig command not found"
ARP_COMMAND_NOT_FOUND = "Somehow 'arp' command were not found"
ARPSPOOF_PERMISSION_DENIED = "You need root permissions to run 'arpspoof'\n         Run with: sudo python3 main.py"
ARPSPOOF_COMMAND_NOT_FOUND = "'arpspoof' is not installed"
INCOMPLETE_DATA = "Some devices were not detected as incomplete, consider re-scan for devices"
STOPPING_ARPSPOOF = "Stopping arpspoof..."
