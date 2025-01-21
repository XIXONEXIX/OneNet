import hashlib
import re

# Sample netstat output as a string (replace with actual netstat output)
netstat_output = """
  Proto  Local Address          Foreign Address        State
  TCP    10.78.158.154:19368    142.250.217.110:443    ESTABLISHED
  TCP    10.78.158.154:19370    172.64.146.215:443     ESTABLISHED
  TCP    10.78.158.154:19371    34.107.243.93:443      ESTABLISHED
  TCP    10.78.158.154:19372    34.107.221.82:80       ESTABLISHED
  TCP    10.78.158.154:19373    34.107.221.82:80       ESTABLISHED
"""

# Regular expression to extract destination IPs from netstat output
ip_pattern = r"\d+\.\d+\.\d+\.\d+"

# Function to compute the checksum of an IP address
def compute_checksum(ip_address):
    # Create a hash object
    hash_object = hashlib.sha256()
    # Update the hash object with the IP address
    hash_object.update(ip_address.encode())
    # Return the checksum as a hexadecimal string
    return hash_object.hexdigest()

# Find all destination IP addresses in the netstat output
destination_ips = re.findall(ip_pattern, netstat_output)

# Compute checksum for each destination IP
ip_checksums = {}
for ip in destination_ips:
    ip_checksums[ip] = compute_checksum(ip)

# Output the checksums for each destination IP
for ip, checksum in ip_checksums.items():
    print(f"IP: {ip}, Checksum: {checksum}")
