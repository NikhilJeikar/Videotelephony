from Client import Client
from Thread import Thread

client = Client("192.168.1.6")
client.Start()
Id = input("Enter the Room ID: ")
Join = f"Join||{Id}|| ||"
client.SendTCP(f"{len(Join)}||{Join}")


def TCP():
    while True:
        print(f"Sent through TCP{client.ReceiveTCP()}")


def UDP():
    while True:
        print(client.ReceiveUDP())


TCP_Thread = Thread(target=TCP, args=())
UDP_Thread = Thread(target=UDP, args=())
TCP_Thread.start()
UDP_Thread.start()
