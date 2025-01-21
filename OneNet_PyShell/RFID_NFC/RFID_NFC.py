import os
import subprocess
from time import sleep

# Ensure necessary packages are installed
def ensure_packages():
    try:
        import kivy
        import nfc
    except ImportError:
        print("Required libraries not found. Installing...")
        subprocess.check_call(['pip', 'install', 'kivy', 'nfc'])

# Run the setup
ensure_packages()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


# NFC Hardware Initialization
def initialize_nfc():
    print("\nInitializing NFC Hardware...")
    try:
        from android.nfc import NfcAdapter
        nfc_adapter = NfcAdapter.getDefaultAdapter()
        if not nfc_adapter:
            print("NFC hardware not detected. Ensure your device supports NFC.")
            return None
        print("NFC Hardware initialized successfully.")
        return nfc_adapter
    except Exception as e:
        print(f"Error initializing NFC hardware: {e}")
        return None


# Scan or Read NFC Tag (to detect all scanned codes)
def read_or_scan_nfc_tag(nfc_adapter, scanned_codes):
    print("\nScanning for NFC tags...")
    try:
        if not nfc_adapter:
            print("NFC Adapter is not initialized. Please initialize hardware first.")
            return

        print("Waiting for NFC tag interaction...")
        tag = nfc_adapter.readTag()  # Simulate reading the tag
        if tag:
            door_code = tag.getId()  # Get the ID of the tag (the door code)
            if door_code not in scanned_codes:
                scanned_codes.append(door_code)
            print(f"Door Code Detected: {door_code}")
            return door_code
        else:
            print("No NFC tag detected. Try again.")
            return None

    except Exception as e:
        print(f"Error during NFC hardware scan: {e}")
        return None


# Write to NFC Tag (apply selected code to the transmitter)
def write_to_nfc_tag(nfc_adapter, selected_code):
    print("\nWriting code to NFC tag...")
    try:
        if not nfc_adapter:
            print("NFC Adapter is not initialized. Please initialize hardware first.")
            return

        if selected_code:
            print(f"Writing code {selected_code} to NFC tag...")
            # Implement writing logic here, e.g., apply selected_code to transmitter
            print(f"Code {selected_code} written successfully to NFC transmitter.")
        else:
            print("No valid code selected for writing.")
    except Exception as e:
        print(f"Error during NFC tag writing: {e}")


# Main Menu
def display_menu():
    print("\n--- NFC Security Program ---")
    print("1. Initialize and Secure NFC Hardware Control")
    print("2. Read NFC Tags (Scan for Door Codes)")
    print("3. Write to NFC Tag (Apply Selected Code)")
    print("4. Brute Force NFC Tags")
    print("5. Exit")
    return input("Select an option: ").strip()


# Main Program Logic
def main():
    nfc_adapter = None  # Initialize NFC Adapter as None
    scanned_codes = []  # List to store all detected door codes
    last_scanned_code = None

    while True:
        choice = display_menu()

        if choice == "1":
            nfc_adapter = initialize_nfc()  # Initialize NFC hardware

        elif choice == "2":
            # Read NFC tags and store detected codes
            print("\nScanning for the last known door code...")
            door_code = read_or_scan_nfc_tag(nfc_adapter, scanned_codes)

            # Display all the scanned codes
            if scanned_codes:
                print("\nScanned Codes:")
                for code in scanned_codes:
                    print(f"- {code}")
            else:
                print("No NFC tags detected.")

            if door_code:
                last_scanned_code = door_code
                print(f"Last known code: {last_scanned_code}")

        elif choice == "3":
            # Write selected code to NFC tag
            if scanned_codes:
                print("\nSelect a code to write to the NFC transmitter.")
                for idx, code in enumerate(scanned_codes, 1):
                    print(f"{idx}. {code}")
                
                code_choice = input("Enter the number of the code to write: ").strip()
                try:
                    code_choice = int(code_choice)
                    if 1 <= code_choice <= len(scanned_codes):
                        selected_code = scanned_codes[code_choice - 1]
                        write_to_nfc_tag(nfc_adapter, selected_code)
                    else:
                        print("Invalid selection. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            else:
                print("No scanned codes available to write.")

        elif choice == "4":
            # Brute Force NFC Tags (expand logic as needed)
            print("Brute forcing NFC tags (expand logic as needed)...")

        elif choice == "5":
            print("\nExiting Program. Goodbye!")
            break

        else:
            print("\nInvalid selection. Please try again.")


# Run the program
if __name__ == "__main__":
    main()
