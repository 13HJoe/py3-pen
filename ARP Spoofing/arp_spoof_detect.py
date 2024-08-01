import scapy.all as scapy
from termcolor import colored

def sniff(interface):
    print(colored('[+] ARP spoofing detector active', 'green'))
    scapy.sniff(iface=interface, 
                store=False, 
                prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        real_mac = get_mac(packet[scapy.ARP].psrc)
        response_mac = packet[scapy.ARP].hwsrc
        if real_mac != response_mac:
            ip = packet[scapy.ARP].psrc
            print(colored("[-] Under Attack ->"+ip+"'s MAC address is being spoofed",'red'))

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    response = scapy.srp(arp_req_broadcast, 
                         timeout=10, 
                         verbose=False)[0] # answered packets [1] -> unanswered packets
    if len(response) == 0:
        print(colored("\n[-] Target ->"+ip+" is down", "yellow"))
        print(colored("[-] POSSIBLE ATTACK",'yellow'))
        exit(0)
    return response[0][1].hwsrc

sniff("WiFi")