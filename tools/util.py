#
# Various utilities
#
from language.language import IPCONFIG_COMMAND_NOT_FOUND
from language.language import ARPSPOOF_PERMISSION_DENIED
from language.language import ARPSPOOF_COMMAND_NOT_FOUND
from language.language import NO_INTERFACES_WERE_FOUND
from language.language import UPDATE_CONNECTED_USERS
from language.language import OPTION_IS_NOT_IN_LIST
from language.language import ARP_COMMAND_NOT_FOUND
from language.language import DISCOVERING_DEVICES
from language.language import SELECT_AN_INTERFACE
from language.language import SELECT_THE_GATEWAY
from language.language import CONFIRM_INTERFACE
from language.language import SELECT_AN_OPTION
from language.language import INCOMPLETE_DATA
from language.language import SELECT_OPTIONS
from language.language import VIEW_AS_MAC
from language.language import VIEW_AS_IP
from language.language import SELECT_ALL
from language.language import FINISH
from tools.arpspoof_thread import ArpSpoofThread
from tools.config_manager import SYS_NAME
from subprocess import Popen
from subprocess import PIPE
from subprocess import run
from re import findall
from re import sub


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
# Makes user select one or more options from list
#
def choose_from_list(options_org, max_items=None) -> list:
    if max_items is None:
        max_items = len(options_org)

    options_list = options_org.copy()
    options_list += [FINISH, SELECT_ALL]

    selected_items = list()

    while len(selected_items) < max_items:
        printable_list, options, options_values = create_options_list(options_list)
        print(printable_list)
        print(SELECT_OPTIONS % (len(selected_items), max_items))
        option = choose_option(options, options_values)
        if option != FINISH and option != SELECT_ALL:
            selected_items.append(option)
            options_list.remove(option)
        elif option == SELECT_ALL:
            return options_org
        else:
            break

    return selected_items


#
# Makes user select one or more threads
#
def choose_threads(arpspoof_threads, options_list) -> list:
    options_list += [FINISH, SELECT_ALL]

    selected_threads_i = list()

    while len(selected_threads_i) < len(arpspoof_threads):
        printable_list, options, options_values = create_options_list(options_list)
        print(printable_list)
        print(SELECT_AN_OPTION)
        option = choose_option(options, options_values)
        if option != FINISH and option != SELECT_ALL:
            for i, thread in enumerate(arpspoof_threads):
                if thread.victim == option:
                    options_list.remove(option)
                    selected_threads_i.append(i)
                    break
        elif option == SELECT_ALL:
            for i in range(len(arpspoof_threads)):
                selected_threads_i.append(i)
            break
        else:
            break

    return selected_threads_i


#
# Runs arp -i [interface] -a
#
def run_arp_a(interface=None) -> str:
    if interface is None:
        # Windows
        process = Popen("arp -a", stdout=PIPE)
    else:
        # Unix and unix-like
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
def arpspoof_available() -> bool:
    try:
        if SYS_NAME == "nt":
            process = run("arpspoof.exe", capture_output=True)
        else:
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
def create_arpspoof_thread(victim, gateway, working_interface=None) -> ArpSpoofThread:
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
# Let's user select a INTERFACE
#
def select_interface() -> str:
    interfaces = retrieve_interfaces()

    working_interface = None

    if not interfaces and SYS_NAME != "nt":
        input(NO_INTERFACES_WERE_FOUND)
        exit(0)
    elif SYS_NAME != "nt":
        printable_list, options, options_values = create_options_list(interfaces)
        confirm_interface = False
        while not confirm_interface:
            print(printable_list)
            print(SELECT_AN_INTERFACE)
            working_interface = choose_option(options, options_values)
            print(CONFIRM_INTERFACE % working_interface)
            confirm_interface = choose_option(["1", "2"], [True, False])

    return working_interface


#
# Gets str-form output from command
# and replaces some things
#
def retrieve_connected_users(interface=None, gateway=None) -> list:
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

    if SYS_NAME == "nt":
        # Looks for any interfaces (listened as IP)
        # Like "Interface: XXX.XXX.XXX.XXX ---"
        interfaces = findall(r"[\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[ ][-]", output)
        for interface in interfaces:
            try:
                interface = interface.replace(" -", "")
                connected_users_ip.remove(interface)
            except ValueError:
                pass

        # Looks for any string like "XX-XX-XX-XX-XX-XX"
        # arp -a for windows uses '-' instead of ':'
        connected_users_mac = findall(r"[\w]{1,2}[-][\w]{1,2}[-][\w]{1,2}[-][\w]{1,2}[-][\w]{1,2}[-][\w]{1,2}", output)
    else:
        # Looks for any string like "XX:XX:XX:XX:XX:XX"
        connected_users_mac = findall(r"[\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}[:][\w]{1,2}", output)

    available_mac = len(connected_users_ip) == len(connected_users_mac)
    if not available_mac:
        print(INCOMPLETE_DATA)

    #
    # Removes gateway if its already defined
    #
    if gateway is not None and gateway in connected_users_ip:
        delete = connected_users_ip.index(gateway)
        connected_users_ip.pop(delete)
        if available_mac:
            connected_users_mac.pop(delete)

    return [available_mac, connected_users_ip, connected_users_mac]


#
# Chooses a single ip
#
def choose_ip(msg, working_interface=None, gateway=None) -> str:
    re_run = True
    view_as_ip = True
    user_address = None
    devices_ip, devices_mac = [], []

    while user_address is None:
        if re_run:
            re_run = False
            print(DISCOVERING_DEVICES)
            show_as_mac, devices_ip, devices_mac = retrieve_connected_users(working_interface, gateway)

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
# Let's user select a GATEWAY
#
def select_gateway(interface) -> str:
    return choose_ip(SELECT_THE_GATEWAY, interface)
