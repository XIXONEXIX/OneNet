import os
import psutil
import logging
import sys

# Setup logging
LOG_FILE = "abnormality_test.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message):
    """Helper function to log and print messages."""
    print(message)
    logging.info(message)

# 1. Registry Check
def check_registry_entries():
    """
    Simulate a registry scan for suspicious entries.
    """
    log_and_print("Checking for suspicious registry entries...")
    # Simulated list of suspicious registry entries
    suspicious_entries = [
        'HKEY_LOCAL_MACHINE\\MaliciousKey',
        'HKEY_CURRENT_USER\\UnwantedEntry'
    ]
    if suspicious_entries:
        log_and_print(f"Suspicious registry entries detected: {suspicious_entries}")
    else:
        log_and_print("No suspicious registry entries detected.")

# 2. Behavior Analysis
def analyze_system_behavior():
    """
    Simulate system behavior analysis for anomalies.
    """
    log_and_print("Checking system behavior for anomalies...")
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    log_and_print(f"CPU={cpu_usage}%, Memory={memory_usage}%, Disk={disk_usage}%")
    if cpu_usage > 80 or memory_usage > 90 or disk_usage > 90:
        log_and_print("Critical system anomaly detected!")
    else:
        log_and_print("System behavior is within normal parameters.")

# 3. Process Monitoring
def monitor_processes():
    """
    Monitor system processes for suspicious activity.
    """
    log_and_print("Scanning running processes...")
    suspicious_processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'exe']):
        try:
            # Simulated suspicious process detection
            if "malware" in (proc.info['name'] or "").lower():
                suspicious_processes.append(proc.info)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    if suspicious_processes:
        log_and_print(f"Suspicious processes detected: {suspicious_processes}")
    else:
        log_and_print("No suspicious processes detected.")

# 4. Debugging and Logging Tools
def debug_and_log():
    """
    Provide user with insights on debugging and runtime events.
    """
    log_and_print("Debug and log tools are active.")
    # Example: Display log file location
    log_and_print(f"Log file saved to: {os.path.abspath(LOG_FILE)}")

# Main Workflow
def main():
    log_and_print("Starting enhanced abnormality test script...")
    try:
        check_registry_entries()
        analyze_system_behavior()
        monitor_processes()
        debug_and_log()
    except Exception as e:
        log_and_print(f"An error occurred: {e}")
        sys.exit(1)

    log_and_print("Abnormality test completed successfully.")

if __name__ == "__main__":
    main()
