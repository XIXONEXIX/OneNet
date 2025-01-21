import os
import pywifi
import time
import subprocess
import speedtest
import psutil

# Initialize the Wi-Fi object
wifi = pywifi.PyWiFi()

# Get the first available interface
def get_wifi_interface():
    interfaces = wifi.interfaces()
    if interfaces:
        return interfaces[0]
    return None

# Function to access device manager and find Wi-Fi adapter specifications
def get_adapter_specs():
    print("\nFetching Wi-Fi adapter specifications from Device Manager...")
    try:
        # PowerShell command to list network adapters and their details
        command = 'powershell Get-WmiObject Win32_NetworkAdapter | Where-Object { $_.AdapterType -eq "Ethernet 802.3" -or $_.AdapterType -eq "Wireless" }'
        output = subprocess.check_output(command, shell=True, text=True)
        print("Device Manager Output:\n")
        print(output)
    except Exception as e:
        print(f"Error accessing Device Manager: {e}")

# Optimize the Wi-Fi for maximum performance (using PowerShell and netsh)
def optimize_wifi():
    wifi_interface = get_wifi_interface()
    if not wifi_interface:
        print("No Wi-Fi interface found.")
        return

    print(f"Found Wi-Fi Interface: {wifi_interface.name()}")

    # Set adapter to maximum performance mode
    try:
        print("Setting Wi-Fi adapter to maximum performance mode...")
        subprocess.call("powercfg -change -standby-timeout-ac 0", shell=True)  # Disable sleep on AC power
        subprocess.call("powercfg -change -monitor-timeout-ac 0", shell=True)  # Disable monitor timeout on AC
        subprocess.call("netsh interface set interface name=\"Wi-Fi\" admin=enabled", shell=True)  # Ensure interface is enabled
        print("Wi-Fi adapter set to maximum performance mode.")
    except Exception as e:
        print(f"Error setting Wi-Fi adapter to max performance: {e}")
    
    # Get available networks
    networks = wifi_interface.scan_results()
    print(f"Networks found: {len(networks)}")

    # Connect to the strongest network
    if networks:
        best_network = max(networks, key=lambda x: x.signal)
        print(f"Best Network: {best_network.ssid}, Signal Strength: {best_network.signal} dBm")
        profile = pywifi.Profile()
        profile.ssid = best_network.ssid
        profile.auth = pywifi.const.AUTH_ALG_OPEN
        profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
        profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
        profile.key = "your_password_here"  # Use your Wi-Fi password
        wifi_interface.connect(profile)
        time.sleep(5)
        print("Successfully connected to the best network.")
    else:
        print("No Wi-Fi networks available.")

# Check Wi-Fi Signal Strength
def check_wifi_signal():
    wifi_interface = get_wifi_interface()
    if not wifi_interface:
        print("No Wi-Fi interface found.")
        return
    
    print(f"Found Wi-Fi Interface: {wifi_interface.name()}")
    networks = wifi_interface.scan_results()
    print(f"Networks found: {len(networks)}")
    
    if networks:
        best_network = max(networks, key=lambda x: x.signal)  # Max signal strength
        print(f"Best Network: {best_network.ssid}, Signal Strength: {best_network.signal} dBm")
    else:
        print("No networks found.")

# Reset Wi-Fi Adapter
def reset_wifi_adapter():
    wifi_interface = get_wifi_interface()
    if not wifi_interface:
        print("No Wi-Fi interface found.")
        return
    
    print(f"Found Wi-Fi Interface: {wifi_interface.name()}")
    try:
        print("Disabling Wi-Fi adapter...")
        subprocess.call(f"netsh interface set interface name=\"{wifi_interface.name()}\" admin=disable", shell=True)
        time.sleep(2)
        print("Re-enabling Wi-Fi adapter...")
        subprocess.call(f"netsh interface set interface name=\"{wifi_interface.name()}\" admin=enable", shell=True)
        print("Wi-Fi adapter reset successfully.")
    except Exception as e:
        print(f"Error resetting Wi-Fi adapter: {e}")

# Run Wi-Fi Speed Test
def run_speed_test():
    print("Running speed test...")
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert from bps to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bps to Mbps
    ping = st.results.ping
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms")

# Main Menu for Interaction
def main_menu():
    while True:
        print("\nWi-Fi Tweaker Runtime - Optimizing Wi-Fi performance!\n")
        print("Choose an option:")
        print("1. Optimize Wi-Fi")
        print("2. Check Wi-Fi Signal")
        print("3. Reset Wi-Fi Adapter")
        print("4. Run Wi-Fi Speed Test")
        print("5. Get Adapter Specs")
        print("6. Exit")
        
        try:
            choice = int(input("Enter option (1-6): "))
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 6.")
            continue
        
        if choice == 1:
            optimize_wifi()
        elif choice == 2:
            check_wifi_signal()
        elif choice == 3:
            reset_wifi_adapter()
        elif choice == 4:
            run_speed_test()
        elif choice == 5:
            get_adapter_specs()
        elif choice == 6:
            print("Exiting Wi-Fi Tweaker Runtime...")
            break
        else:
            print("Invalid choice. Please choose a valid option (1-6).")

# Start the script by calling the main menu
if __name__ == "__main__":
    main_menu()
