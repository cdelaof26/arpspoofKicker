#
# Manager for threads
#
from language.language import THREAD_ENDED_UNEXPECTEDLY
from language.language import THREAD_IS_NOT_RUNNING
from language.language import THREAD_IS_RUNNING
from language.language import DUPLICATED_VICTIM
from language.language import SELECT_A_VICTIM
from language.language import THREAD_CREATED
from language.language import THREAD_V_G
from language.language import STARTING
from language.language import STOPPING
from language.language import DELETING
from tools.util import create_arpspoof_thread
from tools.util import select_interface
from tools.util import select_gateway
from tools.util import choose_threads
from tools.util import choose_ip
from time import sleep


class DoSManager:
    def __init__(self):
        self.INTERFACE = select_interface()
        self.GATEWAY = select_gateway(self.INTERFACE)
        self.arpspoof_threads = list()

    #
    # Checks if there is already a thread pointing to new_victim
    #
    def is_duplicated_victim(self, new_victim) -> bool:
        for thread in self.arpspoof_threads:
            if thread.victim == new_victim and not (thread.terminated or thread.ended_unexpectedly):
                return True
        return False

    #
    # Add a thread to active threads
    #
    def create_thread(self):
        victim = choose_ip(SELECT_A_VICTIM, self.INTERFACE, self.GATEWAY)

        if not self.is_duplicated_victim(victim):
            self.arpspoof_threads.append(create_arpspoof_thread(victim, self.GATEWAY, self.INTERFACE))
            print(THREAD_CREATED)
        else:
            print(DUPLICATED_VICTIM % victim)

    #
    # Let's user select which threads start
    #
    def start_threads(self):
        options_list = list()
        for thread in self.arpspoof_threads:
            # Only not started threads are selectable
            if not thread.is_running:
                options_list.append(thread.victim)

        threads_to_run = choose_threads(self.arpspoof_threads, options_list)

        for thread_i in threads_to_run:
            thread = self.arpspoof_threads[thread_i]
            print(STARTING + THREAD_V_G % (thread.victim, thread.gateway))
            thread.start()
            sleep(0.5)

    #
    # Let's user select which threads stop or delete
    #
    def stop_del_threads(self):
        options_list = list()
        for thread in self.arpspoof_threads:
            # Only started or ended threads are selectable
            if thread.is_running or thread.terminated or thread.ended_unexpectedly:
                options_list.append(thread.victim)

        threads_to_stop = choose_threads(self.arpspoof_threads, options_list)

        while threads_to_stop:
            thread = self.arpspoof_threads[threads_to_stop[-1]]

            if thread.is_running and not (thread.terminated or thread.ended_unexpectedly):
                print(STOPPING + THREAD_V_G % (thread.victim, thread.gateway))
                thread.stop()
                sleep(0.5)
            elif thread.terminated or thread.ended_unexpectedly:
                print(DELETING + THREAD_V_G % (thread.victim, thread.gateway))
                self.arpspoof_threads.remove(thread)
                sleep(0.5)

            threads_to_stop = threads_to_stop[:-1]

    #
    # Prints threads status
    #
    def print_status(self):
        print()
        for thread in self.arpspoof_threads:
            if thread.is_running and not thread.terminated and not thread.ended_unexpectedly:
                print(THREAD_IS_RUNNING % thread.victim)
            elif thread.ended_unexpectedly:
                print(THREAD_ENDED_UNEXPECTEDLY % thread.victim)
            else:
                print(THREAD_IS_NOT_RUNNING % thread.victim)
            sleep(0.5)
        print()

    #
    # Stops all active threads
    #
    def exit_threads(self):
        while self.arpspoof_threads:
            thread = self.arpspoof_threads[-1]
            print(DELETING + THREAD_V_G % (thread.victim, thread.gateway))
            thread.stop()
            self.arpspoof_threads.remove(thread)
            sleep(0.5)
