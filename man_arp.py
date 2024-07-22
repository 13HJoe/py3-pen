import scapy.all as scapy
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser()
    parser.add_argument("-t","--target",dest="target",required=True,help="Target IP for Host Discovery")
    return parser.parse_args()

def parse(answ):
    print("\n\n")
    if len(answ) == 0:
        print("[-] No Live Hosts")
    else:
        print("[+] Found "+str(len(answ))+" live hosts\n")
        print("IP\t\t\t MAC\n---------------------------------------------")
        for ele in answ:
            packet = ele[1]
            print(""+packet.psrc+"\t\t|"+packet.hwsrc)

def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    answ =  scapy.srp(arp_req_broadcast, timeout=1)[0]
    parse(answ)

scan(get_args().target)