from socket import *
from Thread import Thread


class Client:
    def __init__(self, HostIP: str, UDPPort: int = 24680, TCPPort: int = 24682, Buffer: int = 1024 * 64):
        self.__IP = HostIP
        self.__UDPPort = UDPPort
        self.__TCPPort = TCPPort
        self.__TCPSocket = None
        self.__UDPSocket = None
        self.__TCPThread = None
        self.__UDPThread = None
        self.__Buffer = Buffer
        self.__UDPUp = False
        self.__TCPUp = False

    def __InitUDP(self):
        self.__UDPSocket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.__UDPSocket.connect((self.__IP, self.__UDPPort))
        self.__UDPUp = True

    def __InitTCP(self):
        self.__TCPSocket = socket()
        self.__TCPSocket.connect((self.__IP, self.__TCPPort))
        self.__TCPUp = True

    def SendTCP(self, Data):
        self.__TCPSocket.send(Data.encode())

    def SendUDP(self, Data):
        self.__UDPSocket.sendto(Data.encode(), (self.__IP, self.__UDPPort))

    def ReceiveTCP(self):
        return self.__TCPSocket.recv(self.__Buffer)

    def ReceiveUDP(self):
        return self.__UDPSocket.recvfrom(self.__Buffer)

    def __StopTCP(self):
        self.__TCPSocket.close()
        self.__TCPThread.kill()
        self.__TCPSocket = None
        self.__TCPThread = None
        self.__TCPUp = False

    def __StopUDP(self):
        self.__UDPSocket.close()
        self.__UDPThread.kill()
        self.__UDPSocket = None
        self.__UDPThread = None
        self.__UDPUp = False

    def Stop(self):
        self.__StopUDP()
        self.__StopTCP()
        print("Client closed")

    def RestartTCP(self):
        self.__StopTCP()
        self.__InitTCP()

    def RestartUDP(self):
        self.__StopUDP()
        self.__InitUDP()

    def Restart(self):
        self.RestartUDP()
        self.RestartTCP()

    def Start(self):
        print(f"Connecting to {self.__IP}")
        self.__TCPThread = Thread(target=self.__InitTCP)
        self.__TCPThread.start()
        self.__UDPThread = Thread(target=self.__InitUDP)
        self.__UDPThread.start()
        while not self.__TCPUp or not self.__UDPUp:
            pass
        print("Connected")



