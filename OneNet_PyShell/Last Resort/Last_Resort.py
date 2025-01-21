import os
import winreg
import requests
import time
from bs4 import BeautifulSoup
from plyer import notification
import logging
import threading

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def log_and_print(message):
    logging.info(message)

# Example list of malicious registry entries
malicious_registry_entries = [
    'HKEY_LOCAL_MACHINE\\SOFTWARE\\MaliciousSoftware',
    'HKEY_CURRENT_USER\\SOFTWARE\\UnwantedApp'
]

# Scrape a real threat intelligence website for suspicious registry entries
def scrape_registry_entries(url):
    log_and_print(f"Scraping URL: {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Modify according to the actual HTML structure of the threat feed
        registry_entries = soup.find_all('li', class_='registry-entry')  # Example, adjust accordingly
        entries = [entry.get_text() for entry in registry_entries]
        log_and_print(f"Found {len(entries)} suspicious registry entries.")
        return entries
    except Exception as e:
        log_and_print(f"Error scraping {url}: {e}")
        return []

# Fetch threat intelligence data from external sources
def fetch_threat_intelligence():
    log_and_print("Fetching threat intelligence data.")
    entries = []
    threat_sources = [
        "https://example.com/threat-intel-feed",  # Replace with actual threat intel URLs
        "https://www.virustotal.com/en/file/",
        "https://www.ibm.com/security/x-force/",
    ]
    
    # Scrape each source
    for url in threat_sources:
        log_and_print(f"Scraping threat intel from {url}")
        new_entries = scrape_registry_entries(url)
        if new_entries:
            entries.extend(new_entries)
    
    # Return the list of found malicious registry entries
    return entries

# Check the system registry for suspicious entries
def check_registry_entries():
    log_and_print("Checking system registry for suspicious entries.")
    hive_dict = {
        'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
        'HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
        'HKEY_USERS': winreg.HKEY_USERS,
        'HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG,
    }

    for entry in malicious_registry_entries:
        hive, subkey = entry.split("\\", 1)

        try:
            log_and_print(f"Checking registry: {entry}")
            registry_key = winreg.OpenKey(hive_dict[hive], subkey)
            try:
                registry_value = winreg.QueryValueEx(registry_key, '')  # Get the default value
                log_and_print(f"Found suspicious registry entry: {entry}")
                notification.notify(
                    title="Suspicious Registry Entry Found",
                    message=f"Malicious registry entry detected: {entry}",
                    timeout=10
                )
            except FileNotFoundError:
                log_and_print(f"Registry entry not found: {entry}")
            winreg.CloseKey(registry_key)
        except Exception as e:
            log_and_print(f"Error accessing registry entry {entry}: {e}")

# Monitor function to periodically check for new threats
def monitor():
    log_and_print("Starting periodic monitoring...")

    while True:
        # Fetch new threat intelligence
        log_and_print("Fetching new threat intelligence.")
        threat_intel = fetch_threat_intelligence()
        if threat_intel:
            malicious_registry_entries.extend(threat_intel)

        # Check for suspicious entries in the registry
        check_registry_entries()

        # Wait for a specified amount of time before checking again (e.g., 1 hour)
        log_and_print("Waiting for the next check...")
        time.sleep(3600)  # Sleep for 1 hour

# Main execution to run monitoring in a separate thread
def main():
    log_and_print("Last Resort Auto Snooper Script - Started")

    # Run monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.daemon = True  # Allows the thread to exit when the program ends
    monitor_thread.start()

    # Main thread will keep running, waiting for user interruption (Ctrl+C)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_and_print("Last Resort Auto Snooper Script - Interrupted")

if __name__ == "__main__":
    main()
