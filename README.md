
# Port SCanner

**Description**

This is a simple yet powerful port scanner tool built using Python and Scapy. It allows you to scan a range of ports on a target IP address, detect open ports, grab banners, and identify common services running on these ports. The tool features colorful terminal output and a progress bar for an enhanced user experience. It also supports parallel scanning for improved speed and user-friendly input methods.


**Features**

- **Port Scanning:** Scan a specified range of ports on a target IP address.
- **Banner Grabbing:** Fetch service information from open ports.
- **Service Detection:**  Identify common services running on detected ports.
- **Colorful Output: **Distinguish different types of messages with colors.
- **Progress Bar:**Visualize the scanning progress.
- **Parallel Scanning:** Uses multithreading for faster scanning.


**Prerequisites**
- Python 3.x
- Scapy
- Termcolor
- Tqdm

**Installation**
    1. Clone this repository or download the script file:



```git clone https://github.com/abdulaziz-backend/portfunnese```

    2. Navigate to the project directory
    3. Install the required Python packages:
``
    pip install scapy termcolor tqdm
    ``

**Usage**
Run the script from the terminal with the target IP address and optional port range.

**Command Syntax**
```python port_scanner.py <target_ip> -p <port_range>```


**Examples**

Scan ports 1 to 1024 on IP address 192.168.1.1:

```python main.py 192.168.1.1```

Scan ports 20 to 80 on IP address 192.168.1.1:

```python port_scanner.py 192.168.1.1 -p 20-80```

**Interactive Input**

If no target IP is provided in the command line, the script will prompt for the target IP and port range interactively.

**Output Explanation**

- Open Ports: Ports that are open will be displayed in green along with the detected service and banner information, if available.
- Closed Ports: Ports that are closed will be displayed in yellow.
- Warning Messages: Any warning or informational messages will be displayed in yellow.
- Progress Bar: A progress bar will indicate the scanning progress.

**Final Summary**

After scanning, the script will display:

- The list of open ports on the target IP.
- The total number of open ports.


**How It Works**

1. **Port Scanning:** The script sends SYN packets to each port in the specified range and waits for a SYN-ACK response to determine if the port is open.
2. **Banner Grabbing:** If a port is open, the script attempts to connect to the port and retrieve any available banner information.
3. **Service Detection:** The script matches common port numbers to their typical services for better readability.
4. **Parallel Scanning:** Uses ThreadPoolExecutor to scan multiple ports concurrently for faster results

----
==========================================

**Code Structure**

- scan_port(ip, port): Sends a SYN packet to the target port and checks for a SYN-ACK response.
- grab_banner(ip, port): Attempts to connect to an open port and fetches the banner.
- detect_service(port): Identifies the common service running on a port.
- scan_ports(ip, start_port, end_port): Scans a range of ports on the target IP and displays the results.



## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


![Logo]("https://i.ibb.co/C9PTBPV/pixelcut-export-25.png)

