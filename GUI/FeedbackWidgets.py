from threading import Thread

from Logic import PcapLogic


class AsyncPcap2Bin(Thread):

    def __init__(self, master):
        Thread.__init__(self)
        self.master = master
        self.counter = 0

    def change_text(self):
        match self.counter:
            case 0:
                self.master.config(text="Converting pcap to bin.")
            case 1:
                self.master.config(text="Converting pcap to bin..")
            case 2:
                self.master.config(text="Converting pcap to bin...")
        self.counter += 1
        self.counter %= 3
        if PcapLogic.stop_pcap_bool:
            self.master.config(text="Finished converting pcap to bin")
            return
        self.master.after(1000, self.change_text)

    def run(self):
        self.master.after(0, self.change_text)