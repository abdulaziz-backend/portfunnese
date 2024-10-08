import sys
import time
import socket
from scapy.all import *
from termcolor import colored, cprint
from tqdm import tqdm
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import ctypes

ascii_art = r'''

 /$$$$$$$                       /$$           /$$$$$$$$                                                         
| $$__  $$                     | $$          | $$_____/                                                         
| $$  \ $$ /$$$$$$   /$$$$$$  /$$$$$$        | $$    /$$   /$$ /$$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ 
| $$$$$$$//$$__  $$ /$$__  $$|_  $$_/        | $$$$$| $$  | $$| $$__  $$| $$__  $$ /$$__  $$ /$$_____/ /$$__  $$
| $$____/| $$  \ $$| $$  \__/  | $$          | $$__/| $$  | $$| $$  \ $$| $$  \ $$| $$$$$$$$|  $$$$$$ | $$$$$$$$
| $$     | $$  | $$| $$        | $$ /$$      | $$   | $$  | $$| $$  | $$| $$  | $$| $$_____/ \____  $$| $$_____/
| $$     |  $$$$$$/| $$        |  $$$$/      | $$   |  $$$$$$/| $$  | $$| $$  | $$|  $$$$$$$ /$$$$$$$/|  $$$$$$$
|__/      \______/ |__/         \___/        |__/    \______/ |__/  |__/|__/  |__/ \_______/|_______/  \_______/
                                                                                                                
'''

cprint(ascii_art, 'cyan')

def colored_input(prompt, color):
    return input(colored(prompt, color))

parser = argparse.ArgumentParser(description='Simple Port Scanner using Scapy')
parser.add_argument('target', type=str, nargs='?', help='Target IP address')
parser.add_argument('-p', '--ports', type=str, default='1-1024', help='Port range to scan (default: 1-1024)')
args = parser.parse_args()

def scan_port(ip, port):
    syn_packet = IP(dst=ip)/TCP(dport=port, flags='S')
    response = sr1(syn_packet, timeout=1, verbose=0)

    if response is None:
        return False, port
    elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
        rst_packet = IP(dst=ip)/TCP(dport=port, flags='R')
        send(rst_packet, verbose=0)
        return True, port
    else:
        return False, port

def grab_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        s.close()
        return banner.decode().strip()
    except:
        return None

def detect_service(port):
    common_ports = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        3306: 'MySQL',
        3389: 'RDP',
    }
    return common_ports.get(port, 'Unknown')

def scan_ports(ip, start_port, end_port):
    cprint(f'Scanning {ip} from port {start_port} to {end_port}', 'red')
    open_ports = []
    futures = []

    with ThreadPoolExecutor(max_workers=1000) as executor:  # Increased the number of workers for faster scanning
        for port in range(start_port, end_port + 1):
            futures.append(executor.submit(scan_port, ip, port))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning Ports"):
            result, port = future.result()
            if result:
                open_ports.append(port)
                service = detect_service(port)
                banner = grab_banner(ip, port)
                if banner:
                    cprint(f'Port {port} ({service}) is open: {banner}', 'green')
                else:
                    cprint(f'Port {port} ({service}) is open', 'green')
            else:
                cprint(f'Port {port} is closed', 'red')

    if open_ports:
        cprint(f'\nOpen ports on {ip}: {", ".join(map(str, open_ports))}', 'green')
    else:
        cprint(f'\nNo open ports found on {ip}', 'red')

if __name__ == '__main__':
    # Ensure you run the script as Administrator on Windows
    if os.name == 'nt' and not ctypes.windll.shell32.IsUserAnAdmin():
        cprint("Please run the script as Administrator.", 'red')
        sys.exit(1)
    
    target_ip = args.target
    if not target_ip:
        target_ip = colored_input("Enter target IP address: ", "yellow")

    start_port, end_port = [int(port) for port in args.ports.split('-')]
    
    while True:
        scan_ports(target_ip, start_port, end_port)
        choice = colored_input("Do you want to scan another IP address or range of ports? (yes/no): ", "yellow").strip().lower()
        if choice != 'yes':
            break
        target_ip = colored_input("Enter target IP address: ", "yellow")
        ports = colored_input("Enter port range (e.g., 1-1024): ", "yellow")
        start_port, end_port = [int(port) for port in ports.split('-')]
