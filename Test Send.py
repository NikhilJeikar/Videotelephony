from Client import Client
from time import sleep
from Thread import Thread


client = Client("192.168.1.6")
client.Start()
DataTCP = f"Create||ID||"
client.SendTCP(f"{len(DataTCP)}||{DataTCP}")


def TCP():
    while True:
        print(f"Sent through TCP {client.ReceiveTCP()}")


def UDP():
    while True:
        print(f"Sent through UDP {client.ReceiveUDP()}")


TCP_Thread = Thread(target=TCP, args=())
UDP_Thread = Thread(target=UDP, args=())
TCP_Thread.start()
UDP_Thread.start()

for i in range(100):
    DataUDP = f"Sent through UDP {i}|| ||"
    DataTCP = f"Data||Sent through TCP {i}|| "
    client.SendTCP(f"{len(DataTCP)}||{DataTCP}")
    client.SendUDP(DataUDP)
    print(f"Sent Packet {i}")
    sleep(2)
