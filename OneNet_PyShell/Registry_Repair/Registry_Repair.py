import os
import psutil
import socket
import subprocess
import shutil
import requests
import hashlib
from datetime import datetime
from plyer import notification
from sklearn.ensemble import IsolationForest
import logging
import importlib
import sys
import winreg  # Added for registry access

# Setup logging
LOG_FILE = "abnormality_test.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to log and print messages
def log_and_print(message):
    print(message)
    logging.info(message)

# Function to automatically check and install missing packages
def check_and_install(package):
    try:
        importlib.import_module(package)
    except ImportError:
        log_and_print(f"Package {package} is missing. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ['requests', 'psutil', 'plyer', 'sklearn']

# Ensure required packages are installed
for package in required_packages:
    check_and_install(package)

# Machine Learning: Isolation Forest for anomaly detection
anomaly_detector = IsolationForest(contamination=0.1)

def train_anomaly_detector():
    training_data = [
        [10, 40, 30],  # Example: CPU, Memory, Disk usage
        [15, 42, 28],
        [12, 39, 35],
        [13, 41, 33]
    ]
    anomaly_detector.fit(training_data)

# System file repair function
def repair_system_files():
    log_and_print("Repairing system files...")
    try:
        log_and_print("Running System File Checker (sfc /scannow)...")
        subprocess.run(['sfc', '/scannow'], check=True)

        log_and_print("Running DISM to check and repair image...")
        subprocess.run(['DISM', '/Online', '/Cleanup-Image', '/RestoreHealth'], check=True)

        log_and_print("System repair completed.")
    except subprocess.CalledProcessError as e:
        log_and_print(f"Error during system repair: {e}")

# Define suspicious processes, files, and critical system files
suspicious_process_names = ['malware.exe', 'rootkit.exe']
suspicious_file_paths = [
    'C:\\Windows\\system32\\malicious_file.exe',
    'C:\\Program Files\\rootkit.exe'
]
critical_system_files = [
    'C:\\Windows\\system32\\kernel32.dll',
    'C:\\Windows\\system32\\important.exe'
]

# Function to check running processes
def check_processes():
    log_and_print("Checking running processes...")
    for process in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if any(suspicious_name.lower() in process.info['name'].lower() for suspicious_name in suspicious_process_names):
                log_and_print(f"Suspicious process found: {process.info['name']} (PID: {process.info['pid']})")
                terminate_process(process.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        log_and_print(f"Terminated suspicious process with PID: {pid}")
    except Exception as e:
        log_and_print(f"Error terminating process {pid}: {e}")

# Function to check for suspicious files
def check_files():
    log_and_print("Checking for suspicious files...")
    for file_path in suspicious_file_paths:
        if os.path.exists(file_path):
            log_and_print(f"Suspicious file found: {file_path}")
            remove_file(file_path)

def remove_file(file_path):
    try:
        if file_path not in critical_system_files:
            os.remove(file_path)
            log_and_print(f"Deleted suspicious file: {file_path}")
        else:
            log_and_print(f"Skipped critical system file: {file_path}")
    except Exception as e:
        log_and_print(f"Error removing file {file_path}: {e}")

# Function to check actual registry entries
def check_registry_entries():
    log_and_print("Checking registry entries...")
    suspicious_entries = [
        'HKEY_LOCAL_MACHINE\\SOFTWARE\\MaliciousKey',  # Example registry path
        'HKEY_CURRENT_USER\\SOFTWARE\\UnwantedEntry'   # Example registry path
    ]
    
    hive_dict = {
        'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
        'HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
        'HKEY_USERS': winreg.HKEY_USERS,
        'HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG,
    }

    # Loop through each suspicious entry
    for entry in suspicious_entries:
        hive, subkey = entry.split("\\", 1)  # Split the registry path into hive and subkey

        try:
            log_and_print(f"Checking registry: {entry}")
            
            # Open the registry key
            registry_key = winreg.OpenKey(hive_dict[hive], subkey)
            
            try:
                # Try to query the value of the registry key
                registry_value = winreg.QueryValueEx(registry_key, '')  # Get the default value
                log_and_print(f"Found suspicious registry entry: {entry}")
                log_and_print(f"Registry Value: {registry_value}")
                # Optionally, you can remove or fix the entry here if necessary
            except FileNotFoundError:
                log_and_print(f"Registry entry not found: {entry}")
            
            # Close the registry key
            winreg.CloseKey(registry_key)
        
        except Exception as e:
            log_and_print(f"Error accessing registry entry {entry}: {e}")

# Main function
def main():
    log_and_print("Starting abnormality test...")
    try:
        train_anomaly_detector()
        check_processes()
        check_files()
        check_registry_entries()
        repair_system_files()
    except Exception as e:
        log_and_print(f"Error occurred: {e}")
    log_and_print("Abnormality test completed successfully.")

if __name__ == "__main__":
    main()
