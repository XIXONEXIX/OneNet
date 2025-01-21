import os
import re
import subprocess
import time

# Define suspicious activity patterns
SUSPICIOUS_PATTERNS = [
    "Nmap scan",             # Nmap scanning tools
    "Port scanning",         # Common port scanning patterns
    "Brute force attempt",   # Repeated connection attempts
]

BLOCKED_IPS = set()

# Function to monitor network activity using tcpdump
def monitor_network():
    print("Monitoring network activity for suspicious traffic...")
    try:
        # Run tcpdump to capture traffic on all interfaces
        process = subprocess.Popen(
            ["sudo", "tcpdump", "-i", "en0", "-n"],  # en0 is the primary interface
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        while True:
            line = process.stdout.readline().strip()
            if line:
                analyze_traffic(line)
    except KeyboardInterrupt:
        print("\nStopping network monitoring...")
    except Exception as e:
        print(f"Error during monitoring: {e}")

# Function to analyze network traffic
def analyze_traffic(log_line):
    # Look for suspicious patterns
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, log_line, re.IGNORECASE):
            print(f"Suspicious activity detected: {log_line}")
            ip = extract_ip(log_line)
            if ip and ip not in BLOCKED_IPS:
                block_ip(ip)
            break

# Function to extract IP address from log lines
def extract_ip(log_line):
    # Regex to match IP addresses
    match = re.search(r"\d+\.\d+\.\d+\.\d+", log_line)
    return match.group(0) if match else None

# Function to block an IP address using pfctl
def block_ip(ip):
    print(f"Blocking IP: {ip}")
    try:
        BLOCKED_IPS.add(ip)
        # Append rule to pfctl configuration to block the IP
        with open("/etc/pf.blocked", "a") as f:
            f.write(f"block drop in quick on en0 from {ip}\n")
        
        # Reload pfctl configuration
        os.system("sudo pfctl -f /etc/pf.conf")
        os.system("sudo pfctl -e")
        print(f"IP {ip} successfully blocked.")
    except Exception as e:
        print(f"Error blocking IP {ip}: {e}")

# Function to initialize pfctl firewall
def setup_firewall():
    print("Setting up macOS Packet Filter (pfctl)...")
    try:
        # Create a custom pfctl blocklist file
        if not os.path.exists("/etc/pf.blocked"):
            with open("/etc/pf.blocked", "w") as f:
                f.write("# Blocked IPs\n")
        
        # Include blocklist in pfctl configuration
        pf_conf = "/etc/pf.conf"
        with open(pf_conf, "r") as f:
            pf_content = f.read()
        
        if "include \"/etc/pf.blocked\"" not in pf_content:
            with open(pf_conf, "a") as f:
                f.write("\ninclude \"/etc/pf.blocked\"\n")
        
        # Enable pfctl
        os.system("sudo pfctl -f /etc/pf.conf")
        os.system("sudo pfctl -e")
        print("Firewall setup complete.")
    except Exception as e:
        print(f"Error setting up firewall: {e}")

# Main function to start the script
def main():
    print("Intrusion Prevention Script for macOS")
    print("-----------------------------------")
    
    # Ensure the script is run as root
    if os.geteuid() != 0:
        print("This script requires root privileges. Please run it as sudo.")
        return
    
    # Setup firewall
    setup_firewall()
    
    # Start network monitoring
    monitor_network()

if __name__ == "__main__":
    main()
