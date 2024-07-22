import subprocess
from argparse import ArgumentParser

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", required=True, help="New MAC Address")
    return parser.parse_args()

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for interface "+interface+" to "+new_mac)
    try:
        subprocess.check_call(["sudo","ifconfig",interface, "down"])
        subprocess.call(f"sudo ifconfig {interface} hw ether {new_mac}", shell=True)
        subprocess.check_call(["sudo","ifconfig",interface, "up"])
    except subprocess.CalledProcessError as e:
        print("[-] Error: Failed to change MAC address", e)

if __name__ == "__main__":
    args = get_arguments()
    change_mac(args.interface, args.new_mac)
