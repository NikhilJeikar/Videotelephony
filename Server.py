from socket import *
from Thread import Thread


class Server:
    def __init__(self, HostIP: str, UDPPort: int = 24680, TCPPort: int = 24682, Devices: int = 10,
                 Buffer: int = 1024 * 64):
        self.__IP = HostIP
        self.__UDPPort = UDPPort
        self.__TCPPort = TCPPort
        self._TCPSocket = None
        self._UDPSocket = None
        self.__Devices = Devices
        self.__TCPThread = None
        self.__UDPThread = None
        self._Buffer = Buffer
        self.__UDPUp = False
        self.__TCPUp = False

    def __InitUDP(self):
        self._UDPSocket = socket(AF_INET, SOCK_DGRAM)
        self._UDPSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._UDPSocket.bind((self.__IP, self.__UDPPort))
        self.__UDPUp = True
        while True:
            Data, Address = self._UDPSocket.recvfrom(self._Buffer)
            self._UDPProcessing(Data, Address[0])

    def __InitTCP(self):
        self._TCPSocket = socket(AF_INET, SOCK_STREAM)
        self._TCPSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._TCPSocket.bind((self.__IP, self.__TCPPort))
        self._TCPSocket.listen(self.__Devices)
        self.__TCPUp = True
        while True:
            Client, Address = self._TCPSocket.accept()
            thread = Thread(target=self._TCPProcessing, args=(Client, Address[0]))
            thread.Bind(self.__TCPThread)
            thread.start()

    def _TCPProcessing(self, Client, Address):
        Data = "Init"
        while len(Data):
            Data = Client.recv(self._Buffer).decode()
            print(Data)

    def _UDPProcessing(self, Data, Address):
        print(Data.decode(), Address)

    def __StopTCP(self):
        self._TCPSocket.close()
        self.__TCPThread.kill()
        self._TCPSocket = None
        self.__TCPThread = None
        self.__TCPUp = False

    def __StopUDP(self):
        self._UDPSocket.close()
        self.__UDPThread.kill()
        self._UDPSocket = None
        self.__UDPThread = None
        self.__UDPUp = False

    def Stop(self):
        self.__StopUDP()
        self.__StopTCP()

    def RestartTCP(self):
        self.__StopTCP()
        print("Starting TCP server")
        self.__TCPThread = Thread(target=self.__InitTCP)
        self.__TCPThread.start()
        while not self.__TCPUp:
            pass
        print("TCP server started")

    def RestartUDP(self):
        self.__StopUDP()
        print("Starting UDP server")
        self.__UDPThread = Thread(target=self.__InitUDP)
        self.__UDPThread.start()
        while not self.__UDPUp:
            pass
        print("UDP server started")

    def Restart(self):
        self.RestartUDP()
        self.RestartTCP()

    def Start(self):
        print(f"Starting server in {self.__IP}")
        print("Starting TCP server")
        self.__TCPThread = Thread(target=self.__InitTCP)
        self.__TCPThread.start()
        while not self.__TCPUp:
            pass
        print("TCP server started")
        print("Starting UDP server")
        self.__UDPThread = Thread(target=self.__InitUDP)
        self.__UDPThread.start()
        while not self.__UDPUp:
            pass
        print("UDP server started")
