- Commands to change MAC address
	- `ifconfig <interface> down` - Disable Interface
	- `ifconfig <interface> hw ether <new_mac_address>`
	- `ifconfig <interface> up` - Enable Interface
- `subprocess` - module [to run sys. commands]
	- ```
	  import subprocess
	  subprocess.call("<command>", Shell=True)
	  ```
