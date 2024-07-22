- Address Resolution Protocol
	- ARP Request - Broadcast
	  collapsed:: true
		- ![image.png](../assets/image_1721647131179_0.png)
	- ARP Response - Unicast [from the device with the specified MAC address]
	  collapsed:: true
		- ![image.png](../assets/image_1721647176215_0.png)
- `scapy` - Module
- <u>ARPing-based scan</u>
  collapsed:: true
	- ```
	  import scapy.all as scapy
	  
	  def scan(ip):
	  	print(scapy.arping(ip))
	  
	  scan("192.168.1.1/24")
	  ```
	- ![image.png](../assets/image_1721654181607_0.png)
- **Manual**
  collapsed:: true
	- 1. Create ARP request directed to broadcast MAC asking for IP
		- ARP-Request : `arp_req = scapy.ARP(pdst=ip)` asking for `ip`
		- To print fields of packet : `scapy.ls(scapy.ARP())`
		- *set DEST. mac to BROADCAST*
			- Creating an broadcast frame - `broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #Ether object`
		- Merge L3 and L2 - `arp_req_broadcast = broadcast/arp_req`
	- 2. Send packet and receive response.`
		- `response = scapy.srp(arp_req_broadcast)`
		- response -> tuple of 2 lists (answered packets[], unanswered packets [])
	- 3. Parse the response.
	  4. Print result.
-
