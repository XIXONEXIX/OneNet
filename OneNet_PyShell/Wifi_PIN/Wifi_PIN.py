import subprocess
import time
import os
import sys


def install_required_packages():
    """
    Checks and installs required Python packages.
    """
    required_packages = ['pywifi']
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


install_required_packages()

from pywifi import PyWiFi, const, Profile


def execute_command(command):
    """
    Executes a shell command and logs its output for debugging.
    """
    try:
        print(f"Executing: {command}")
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
        print(f"Command Output:\n{result}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e.output.decode()}")
        return None


def set_maximum_performance(interface):
    """
    Sets the Wi-Fi adapter to maximum performance by disabling power-saving modes.
    """
    print(f"Configuring {interface} for maximum performance...")
    execute_command(f"powercfg -change standby-timeout-ac 0")  # Disable system sleep
    execute_command(f"netsh interface set interface \"{interface}\" admin=disable")
    time.sleep(1)
    execute_command(f"netsh interface set interface \"{interface}\" admin=enable")
    print(f"Performance settings applied to {interface}.")


def get_network_info():
    """
    Retrieves detailed information about the Wi-Fi network connection.
    """
    print("Fetching current network information...")
    result = execute_command("netsh wlan show interfaces")
    if not result:
        return {}

    network_info = {}
    for line in result.splitlines():
        if "SSID" in line and "BSSID" not in line:
            network_info["SSID"] = line.split(":")[1].strip()
        elif "BSSID" in line:
            network_info["BSSID"] = line.split(":")[1].strip()
        elif "Signal" in line:
            network_info["Signal Strength"] = int(line.split(":")[1].strip().replace('%', ''))
        elif "State" in line:
            network_info["State"] = line.split(":")[1].strip()
    return network_info


def connect_to_wifi_with_pywifi(ssid, password):
    """
    Fallback method: Uses the pywifi library to connect to the Wi-Fi network.
    """
    print(f"Attempting to connect to {ssid} using pywifi...")
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)

    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(10)

    if iface.status() == const.IFACE_CONNECTED:
        print(f"Successfully connected to {ssid}.")
    else:
        print(f"Failed to connect to {ssid} using pywifi.")


def lock_wifi_connection(interface, network_ssid, password=None, min_signal_strength=50):
    """
    Locks the Wi-Fi connection to the specified SSID to prevent drop-offs or disconnections.
    """
    set_maximum_performance(interface)

    while True:
        time.sleep(5)  # Check connection status every 5 seconds
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console for updates

        network_info = get_network_info()
        if not network_info:
            print("Failed to retrieve network information.")
            if password:
                connect_to_wifi_with_pywifi(network_ssid, password)
            continue

        print("\nCurrent Network Info:")
        for key, value in network_info.items():
            print(f"{key}: {value}")

        signal_strength = network_info.get("Signal Strength", 0)
        if signal_strength < min_signal_strength:
            print(f"Signal strength below {min_signal_strength}%. Attempting to reconnect...")
            execute_command(f"netsh wlan connect name=\"{network_ssid}\"")

        current_ssid = network_info.get("SSID", "")
        if current_ssid != network_ssid:
            print(f"Disconnected from {network_ssid}. Reconnecting...")
            execute_command(f"netsh wlan connect name=\"{network_ssid}\"")
            if password:
                connect_to_wifi_with_pywifi(network_ssid, password)
        else:
            print(f"Connected to {network_ssid}. Signal strength: {signal_strength}%.")


# Using 'SeedGuest' as the Wi-Fi password
lock_wifi_connection('Wi-Fi 2', 'Seed Guest', password='SeedGuest')
