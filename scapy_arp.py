import scapy.all as scapy

def scan(ip):
    print(scapy.arping(ip))

scan("192.168.1.1/24")