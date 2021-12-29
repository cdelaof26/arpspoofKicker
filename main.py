from language.language import FOR_ARPSPOOF_CHECK_THIS
from language.language import SELECT_AN_OPTION
from language.language import WELCOME
from language.language import MENU_1
from language.language import MENU
from tools.util import arpspoof_available
from tools.util import choose_option
from tools.config_manager import SYS_NAME
from tools.thread_manager import DoSManager

print(WELCOME)

if not arpspoof_available():
    if SYS_NAME == "nt":
        print(FOR_ARPSPOOF_CHECK_THIS % "https://github.com/alandau/arpspoof")
    elif SYS_NAME == "Darwin":
        print(FOR_ARPSPOOF_CHECK_THIS % "https://ports.macports.org/port/dsniff/")
    else:
        print(FOR_ARPSPOOF_CHECK_THIS % "https://command-not-found.com/dsniff")
    exit(0)


tM = DoSManager()

while True:
    if not tM.arpspoof_threads:
        print(MENU)
        print(SELECT_AN_OPTION)
        option = choose_option(["1", "2", "E"])
    else:
        print(MENU_1)
        print(SELECT_AN_OPTION)
        option = choose_option(["1", "2", "3", "4", "5", "E"])

    if option == "E":
        tM.exit_threads()
        break

    if option == "1":
        tM.create_thread()

    if option == "2":
        print("WIP")

    if option == "3":
        tM.start_threads()

    if option == "4":
        tM.stop_del_threads()

    if option == "5":
        tM.print_status()

print("Bye")
exit(0)
