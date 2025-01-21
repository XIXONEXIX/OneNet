import os
import psutil
import hashlib
import time
import socket

# Function to get the hash of a file
def file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

# Function to check processes
def check_processes():
    print("Checking running processes...")
    suspicious_processes = []

    for proc in psutil.process_iter(attrs=['pid', 'name', 'exe', 'username']):
        try:
            # Gather process information
            pid = proc.info['pid']
            name = proc.info['name']
            exe = proc.info['exe'] or "N/A"
            user = proc.info['username']

            # Calculate file hash
            file_hash_val = file_hash(exe) if exe != "N/A" else None

            # Analyze suspicious activity (basic rules for demo)
            if not os.path.exists(exe):
                suspicious_processes.append((pid, name, user, "Executable path doesn't exist"))
            elif file_hash_val is None:
                suspicious_processes.append((pid, name, user, "Unable to hash executable"))
            elif "temp" in exe.lower() or "appdata" in exe.lower():
                suspicious_processes.append((pid, name, user, "Running from suspicious directory"))

        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue  # Skip processes we can't access

    if suspicious_processes:
        print("\nSuspicious Processes Found:")
        for sp in suspicious_processes:
            pid, name, user, reason = sp
            print(f"PID: {pid}, Name: {name}, User: {user}, Reason: {reason}")

            # Trace network activity for the process
            trace_network(pid)
    else:
        print("No suspicious processes detected.")

# Function to trace network activity for a process
def trace_network(pid):
    try:
        process = psutil.Process(pid)
        connections = process.connections(kind='inet')  # Fetch network connections (TCP/UDP)
        if connections:
            print(f"  Tracing network activity for PID {pid}:")
            for conn in connections:
                local_ip, local_port = conn.laddr if conn.laddr else ("N/A", "N/A")
                remote_ip, remote_port = conn.raddr if conn.raddr else ("N/A", "N/A")
                status = conn.status
                print(f"    Local: {local_ip}:{local_port} -> Remote: {remote_ip}:{remote_port} (Status: {status})")

                # Attempt reverse DNS lookup for remote IP
                if remote_ip != "N/A":
                    try:
                        hostname = socket.gethostbyaddr(remote_ip)[0]
                        print(f"      Remote hostname: {hostname}")
                    except socket.herror:
                        print(f"      Remote hostname: [Could not resolve]")
        else:
            print(f"  No active network connections for PID {pid}.")
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        print(f"  Unable to trace network activity for PID {pid} due to insufficient permissions or process termination.")

if __name__ == "__main__":
    while True:
        check_processes()
        print("\nSleeping for 60 seconds...\n")
        time.sleep(60)  # Check every minute
