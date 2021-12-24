#
# Various utilities
#
from language.language import IPCONFIG_COMMAND_NOT_FOUND
from language.language import ARPSPOOF_PERMISSION_DENIED
from language.language import ARPSPOOF_COMMAND_NOT_FOUND
from language.language import UPDATE_CONNECTED_USERS
from language.language import OPTION_IS_NOT_IN_LIST
from language.language import ARP_COMMAND_NOT_FOUND
from language.language import DISCOVERING_DEVICES
from language.language import INCOMPLETE_DATA
from language.language import VIEW_AS_MAC
from language.language import VIEW_AS_IP

from language.language import DELETE_THREAD
from language.language import STOP_THREAD
from language.language import STOPPING
from language.language import THREAD_V_G

from tools.arpspoof_thread import ArpSpoofThread
from tools.config_manager import SYS_NAME
from subprocess import Popen
from subprocess import PIPE
from subprocess import run
from re import findall
from re import sub
from time import sleep


#
# Makes user select an option
#
def choose_option(options, options_values=None):
    option = None
    while option not in options:
        option = input("> ").upper()
        if option not in options:
            print(OPTION_IS_NOT_IN_LIST % options)

    if options_values:
        return options_values[options.index(option)]

    return option


#
# Converts a list into choose-able list
#
def create_options_list(options_list) -> list:
    printable_list = ""
    options = list()
    options_values = list()
    for i, option in enumerate(options_list):
        printable_list += "\n" + str(i) + ". " + str(option)
        options.append(str(i))
        options_values.append(str(option))

    return [printable_list, options, options_values]


#
# Runs arp -i [interface] -a
#
def run_arp_a(interface=None) -> str:
    if SYS_NAME == "nt":
        process = Popen("arp -a", stdout=PIPE)
    else:
        process = Popen(["arp", "-i", interface, "-a"], stdout=PIPE)

    return (process.communicate()[0]).decode("utf-8")


#
# Runs "ifconfig" command
#
def run_ifconfig() -> str:
    process = Popen("ifconfig", stdout=PIPE)
    return (process.communicate()[0]).decode("utf-8")


#
# Runs "ip a" command
#
def run_ip_a() -> str:
    process = Popen(["ip", "a"], stdout=PIPE)
    return (process.communicate()[0]).decode("utf-8")


#
# Checks if arpspoof command exist
#
def check_arpspoof() -> bool:
    try:
        process = run("arpspoof", capture_output=True)
        output = process.stderr.decode("utf-8")
        if "found" in output:
            print(ARPSPOOF_COMMAND_NOT_FOUND)
            return False

        if "denied" in output:
            print(ARPSPOOF_PERMISSION_DENIED)
            return False

        return True
    except (FileNotFoundError, NotADirectoryError):
        print(ARPSPOOF_COMMAND_NOT_FOUND)
        return False


#
# Runs arpspoof
#
def run_single_arpspoof(victim, gateway, working_interface=None) -> ArpSpoofThread:
    return ArpSpoofThread(victim, gateway, working_interface)
    # process.start()
    # process.stop()


#
# Gets str-form output from command
# and replaces some things
#
def retrieve_interfaces() -> list:
    if SYS_NAME == "nt":
        return list()
    try:
        if SYS_NAME == "Darwin":
            output = run_ifconfig()
        else:
            output = run_ip_a()
    except FileNotFoundError:
        print(IPCONFIG_COMMAND_NOT_FOUND)
        return list()

    # Converts \n and \t into its representation
    output = sub(r"[\\]+[n]", "\n", output)
    output = sub(r"[\\]+[t]", "    ", output)

    # Looks for any string like "en0: " and/or "bridge0: "
    interfaces = findall(r"[a-zA-Z]{2,6}[\d][:][ ]", output)

    # Looks for any string like "enp0s1: "
    interfaces += findall(r"[a-zA-Z]{2,6}[\d][a-zA-Z][\d][:][ ]", output)

    # Removes spaces
    while " " in interfaces:
        interfaces.remove(" ")

    # Removes ": " from strings
    i = 0
    while i < len(interfaces):
        interfaces[i] = sub(r"[: ]", "", interfaces[i])
        i += 1

    return interfaces


#
# Gets str-form output from command
# and replaces some things
#
def retrieve_connected_users(interface=None) -> list:
    try:
        output = run_arp_a(interface)
    except FileNotFoundError:
        print(ARP_COMMAND_NOT_FOUND)
        return [False, [], []]

    # Converts \n and \t into its representation
    output = sub(r"[\\]+[n]", "\n", output)
    output = sub(r"[\\]+[t]", "    ", output)

    # Looks for any string like "192.168.XXX.XXX"
    connected_users_ip = findall(r"[\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}", output)

    # Looks for any string like "XX:XX:XX:XX:XX:XX"
    connected_users_mac = findall(r"[\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}", output)

    available_mac = len(connected_users_ip) == len(connected_users_mac)
    if not available_mac:
        print(INCOMPLETE_DATA)

    return [available_mac, connected_users_ip, connected_users_mac]


#
# Chooses a single ip
#
def choose_ip(msg, working_interface=None) -> str:
    re_run = True
    view_as_ip = True
    user_address = None
    devices_ip, devices_mac = [], []

    while user_address is None:
        if re_run:
            re_run = False
            print(DISCOVERING_DEVICES)
            show_as_mac, devices_ip, devices_mac = retrieve_connected_users(working_interface)

            if show_as_mac:
                devices_ip += [VIEW_AS_MAC, UPDATE_CONNECTED_USERS]
                devices_mac += [VIEW_AS_IP, UPDATE_CONNECTED_USERS]
            else:
                devices_ip += [UPDATE_CONNECTED_USERS]

        if view_as_ip:
            printable_list, options, options_values = create_options_list(devices_ip)
        else:
            printable_list, options, options_values = create_options_list(devices_mac)

        print(printable_list)
        print(msg)
        user_address = choose_option(options, options_values)
        if user_address == UPDATE_CONNECTED_USERS:
            re_run = True
            user_address = None
        elif user_address == VIEW_AS_IP:
            view_as_ip = True
            user_address = None
        elif user_address == VIEW_AS_MAC:
            view_as_ip = False
            user_address = None

    if view_as_ip:
        return user_address
    else:
        return devices_ip[devices_mac.index(user_address)]


#
# Stops all active threads
#
def exit_end_threads(arpspoof_threads):
    while 0 < len(arpspoof_threads):
        thread = arpspoof_threads[0]
        if thread.is_running and not (thread.terminated or thread.ended_unexpectedly):
            print(STOPPING + THREAD_V_G % (thread.victim, thread.gateway))
            thread.stop()
            sleep(1)
        arpspoof_threads.remove(thread)


#
# Basic management for threads
#
def manage_threads(arpspoof_threads):
    end_all = False
    delete_all = False
    thread_i = 0
    while thread_i < len(arpspoof_threads):
        thread = arpspoof_threads[thread_i]

        if thread.is_running and not (thread.terminated or thread.ended_unexpectedly):
            end_current = end_all
            if not end_current:
                print(STOP_THREAD % thread.victim)
                end_current = choose_option(["1", "2", "3"], [True, False, "all"])
                if end_current == "all":
                    end_current = True
                    end_all = True

            if end_current:
                print(STOPPING + THREAD_V_G % (thread.victim, thread.gateway))
                thread.stop()
                arpspoof_threads.remove(thread)
                sleep(1)
            else:
                thread_i += 1
        else:
            delete_current = delete_all or (thread.is_running and (thread.terminated or thread.ended_unexpectedly))
            if not delete_current:
                print(DELETE_THREAD % thread.victim)
                delete_current = choose_option(["1", "2", "3"], [True, False, "all"])
                if delete_current == "all":
                    delete_current = True
                    delete_all = True

            if delete_current:
                arpspoof_threads.remove(thread)
            else:
                thread_i += 1


#
# Checks if there is already a thread pointing to new_victim
#
def is_duplicated_victim(arpspoof_threads, new_victim) -> bool:
    for t in arpspoof_threads:
        if t.victim == new_victim and not (t.terminated or t.ended_unexpectedly):
            return True
    return False
