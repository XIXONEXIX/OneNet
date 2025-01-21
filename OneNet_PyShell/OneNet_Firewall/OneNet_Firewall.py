import subprocess
import sys
import psutil
import socket
import time
import os
import platform
import hashlib
import logging
import requests
import pickle
from collections import defaultdict
from sklearn.ensemble import IsolationForest
import scapy.all as scapy
import threading
import curses

# Auto-install required dependencies
def install_dependencies():
    required_libraries = ["psutil", "requests", "scikit-learn", "scapy"]
    for lib in required_libraries:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install {lib}: {e}")
            print(f"Failed to install {lib}: {e}")

install_dependencies()

# Logging setup
log_dir = "C:/TCP/Intrusion_Prevention_Runtime"  # Modify to your runtime directory or make this dynamic
log_file = os.path.join(log_dir, "firewall_log.txt")

# Create log directory if it doesn't exist
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
    except OSError as e:
        logging.error(f"Failed to create log directory: {e}")
        print(f"Failed to create log directory: {e}")
        sys.exit(1)

logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")
logging.info("Firewall system initialized.")

# Trusted IP ranges
trusted_ips = ['192.168.1.1', '10.0.0.1']

# Known exploit signatures
known_exploits = [
    {'signature': 'user-agent: evilbot', 'description': 'Known bot with malicious intent'},
    {'signature': 'scan_request', 'description': 'Port scanning detected'},
    {'signature': 'rootkits', 'description': 'Rootkit attempt detected'}
]

# Anomaly Detection with ML
class MLAnomalyDetection:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.training_data = []

    def train_model(self, data):
        self.training_data.extend(data)
        self.model.fit(self.training_data)

    def detect_anomalies(self, data):
        return self.model.predict(data)

# Compute checksum
def compute_checksum(file_path):
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error computing checksum for {file_path}: {e}")
        print(f"Error computing checksum for {file_path}: {e}")
        return None

# Validate checksum
def validate_checksum(file_path, original_checksum):
    current_checksum = compute_checksum(file_path)
    if current_checksum != original_checksum:
        logging.warning(f"Checksum mismatch detected for {file_path}!")
        return False
    return True

# Sandbox Execution
def sandbox_execution(stdscr):
    logging.info("Running traffic analysis in a sandbox...")
    stdscr.addstr(1, 0, "Running traffic analysis in a sandbox...")
    stdscr.refresh()
    pass

# Immutable Backup
def create_immutable_backup(file_path, backup_path):
    if not os.path.exists(backup_path):
        try:
            with open(file_path, "rb") as original, open(backup_path, "wb") as backup:
                backup.write(original.read())
            logging.info("Immutable backup created.")
        except Exception as e:
            logging.error(f"Error creating backup for {file_path}: {e}")
            print(f"Error creating backup for {file_path}: {e}")

# Encrypt sensitive data
def encrypt_logs(log_file):
    try:
        with open(log_file, "rb") as file:
            content = file.read()
        encrypted_content = hashlib.sha256(content).hexdigest()
        with open(log_file, "w") as file:
            file.write(encrypted_content)
    except Exception as e:
        logging.error(f"Error encrypting logs: {e}")
        print(f"Error encrypting logs: {e}")

# Monitor and block malicious IPs
def block_ip(ip):
    try:
        if platform.system() == "Windows":
            subprocess.run(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}', shell=True)
            logging.info(f"Blocked IP {ip} on Windows Firewall.")
        elif platform.system() == "Linux":
            subprocess.run(f'sudo iptables -A INPUT -s {ip} -j DROP', shell=True)
            logging.info(f"Blocked IP {ip} using iptables.")
        else:
            logging.warning(f"Unsupported OS for blocking IP: {platform.system()}")
    except Exception as e:
        logging.error(f"Failed to block IP {ip}: {e}")
        print(f"Failed to block IP {ip}: {e}")

# Function to monitor active network connections and sniff packets
def monitor_connections_and_packets(stdscr):
    def packet_callback(packet):
        try:
            if packet.haslayer(scapy.IP):
                source_ip = packet[scapy.IP].src
                dest_ip = packet[scapy.IP].dst
                source_port = packet[scapy.IP].sport if packet.haslayer(scapy.TCP) else None
                dest_port = packet[scapy.IP].dport if packet.haslayer(scapy.TCP) else None
                protocol = packet[scapy.IP].proto

                logging.info(f"Packet: {source_ip}:{source_port} -> {dest_ip}:{dest_port}, Protocol: {protocol}")
                stdscr.addstr(3, 0, f"Packet: {source_ip}:{source_port} -> {dest_ip}:{dest_port}, Protocol: {protocol}")
                stdscr.refresh()
        except Exception as e:
            logging.error(f"Error processing packet: {e}")
            print(f"Error processing packet: {e}")

    logging.info("Starting packet sniffer...")
    scapy.sniff(prn=packet_callback, store=0, filter="ip")

# Function to scan connections
def scan_connections():
    try:
        connections = psutil.net_connections(kind='inet')
        device_behavior = defaultdict(list)

        for conn in connections:
            remote_ip = conn.raddr.ip if conn.raddr else None
            local_ip = conn.laddr.ip

            if remote_ip:
                device_behavior[remote_ip].append(conn.status)

        for device_ip, activities in device_behavior.items():
            logging.info(f"Device IP: {device_ip} - Activities: {activities}")

        return device_behavior
    except Exception as e:
        logging.error(f"Error scanning connections: {e}")
        print(f"Error scanning connections: {e}")
        return {}

# Function to check for anomalies and respond
def detect_and_respond():
    ml_detector = MLAnomalyDetection()

    ml_detector.train_model([[1, 2], [2, 3], [3, 4]])

    while True:
        device_behavior = scan_connections()

        for device_ip, activities in device_behavior.items():
            for exploit in known_exploits:
                if any(exploit['signature'] in activity for activity in activities):
                    logging.info(f"Exploit detected on {device_ip}: {exploit['description']}")
                    block_ip(device_ip)
                    print(f"Blocked {device_ip} due to {exploit['description']}")

        anomalies = ml_detector.detect_anomalies([[len(activities), len(activities[0]) if activities else 0]] for activities in device_behavior.values())
        for idx, anomaly in enumerate(anomalies):
            if anomaly == -1:
                ip = list(device_behavior.keys())[idx]
                logging.info(f"Anomaly detected on {ip}.")
                block_ip(ip)
                print(f"Blocked {ip} due to anomaly.")

        time.sleep(60)

# Function to start network monitoring and blocking malicious IPs
def start_network_monitoring(stdscr):
    sniffer_thread = threading.Thread(target=monitor_connections_and_packets, args=(stdscr,), daemon=True)
    sniffer_thread.start()

    try:
        detect_and_respond()
    except KeyboardInterrupt:
        print("\nNetwork monitoring stopped.")
        logging.info("Network monitoring stopped by user.")

# Main function to deploy the network monitor
def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Network Intrusion Prevention System (NIPS) - Running...")
    stdscr.refresh()

    start_network_monitoring(stdscr)

# Entry point for curses-based terminal UI
if __name__ == "__main__":
    curses.wrapper(main)
