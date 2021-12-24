from language.language import THREAD_ENDED_UNEXPECTEDLY
from subprocess import DEVNULL
from subprocess import STDOUT
from subprocess import Popen
from threading import Thread


class ArpSpoofThread(Thread):
    def __init__(self, victim, gateway, working_interface=None):
        Thread.__init__(self)
        self.victim = victim
        self.gateway = gateway
        self.working_interface = working_interface
        self.process = None
        self.terminated = False
        self.is_running = False
        self.ended_unexpectedly = False

    def run(self):
        self.is_running = True
        self.process = Popen(["arpspoof", "-i", self.working_interface, "-t", self.victim, self.gateway],
                             stdout=DEVNULL, stderr=STDOUT)
        self.process.wait()
        #
        # If arpspoof cannot start or somehow stopped, next code will be reached
        #
        if not self.terminated:
            self.ended_unexpectedly = True
            print(THREAD_ENDED_UNEXPECTEDLY % self.victim)

    def stop(self):
        self.terminated = True
        self.process.terminate()
