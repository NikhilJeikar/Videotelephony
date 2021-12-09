from collections import defaultdict
from Server import Server
import random


class Status:
    Invalid = "Invalid"
    Ack = "Ack"
    Wait = "Wait"
    Close = "Close"


class Header:
    Create = "Create"
    Join = "Join"
    Data = "Data"
    Split = "||"


class Core(Server):
    def __init__(self, IP: str):
        super().__init__(IP, Devices=1000)
        self.__MeetingsID = []
        self.__Meetings = defaultdict(list)
        self.__Address2ID = {}
        self.__AddressTable = {}
        self.__ClientUDPPort = 24680

        self.OnTextReceive = self.__TextReceived
        self.OnVideoReceive = self.__VideoReceived

    def __TextReceived(self, ID, Text):
        for i in Text:
            print(i)
        for i in self.__Meetings[ID]:
            for j in Text:
                self.__AddressTable[i].send(j.encode())

    def __VideoReceived(self, ID, Data, Address):
        if ID is not None:
            for i in self.__Meetings[ID]:
                print("Enter", Data, (i, self.__ClientUDPPort))
                self._UDPSocket.sendto(Data, (i, self.__ClientUDPPort))
        else:
            self._UDPSocket.sendto(Status.Invalid.encode(), Address)

    def _TCPProcessing(self, Client, Address):
        self.__AddressTable[Address] = Client

        def Read():
            Buffer = ""
            Size = None
            Request = "Init"
            while len(Request):
                Request = Client.recv(self._Buffer).decode()
                Buffer += Request
                if Size is None:
                    try:
                        Size, Buffer = Buffer.split(Header.Split, maxsplit=1)
                        Size = int(Size)
                    except ValueError:
                        pass
                if Size is not None:
                    if Size - len(Buffer) <= 0:
                        return Buffer
            return Buffer

        ID = None
        while True:
            KeyWord, Dat = Read().split(Header.Split, maxsplit=1)
            if KeyWord == Header.Create:
                while True:
                    Id = random.randint(0, 10000)
                    if Id not in self.__MeetingsID:
                        ID = Id
                        break
                self.__MeetingsID.append(ID)
                self.__Address2ID[Address] = ID
                self.__Meetings[ID] = []
                Client.send((Status.Ack + Header.Split + str(ID)).encode())
            elif KeyWord == Header.Join:
                ID, = Dat.split(Header.Split, maxsplit=1)
                ID = int(ID)
                self.__Address2ID[Address] = ID
                print("Data", ID)
                if ID in self.__MeetingsID:
                    self.__Meetings[ID].append(Address)
                    self.__Meetings[ID] = list(set(self.__Meetings[ID]))
                    Client.send(Status.Ack.encode())
                else:
                    Client.send(Status.Invalid.encode())
            elif KeyWord == Header.Data:
                Text = Dat.split('\n')
                self.OnTextReceive(ID, Text)
                Client.send(Status.Ack.encode())
            elif KeyWord == Status.Close:
                if ID in self.__MeetingsID:
                    for i in self.__Meetings[ID]:
                        self.__AddressTable[i].close()
                        self.__AddressTable.pop(i)
                    self.__MeetingsID.remove(ID)
                self.__Address2ID.pop(Address)
                self.__Meetings[ID].remove(ID)
                break
            else:
                Client.send(Status.Invalid.encode())

    def _UDPProcessing(self, Data, Address):
        print(Data.decode(), Address)
        ID = self.__Address2ID.get(Address)
        self.OnVideoReceive(ID, Data, Address)


server = Core("192.168.1.6")
server.Start()
