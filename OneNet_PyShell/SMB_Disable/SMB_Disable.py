import subprocess
import sys

# Function to run PowerShell commands
def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        print(f"Command Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")

# Disabling SMBv1 and SMBv2 via PowerShell commands
def disable_smb():
    print("Disabling SMBv1...")
    run_powershell_command('Set-SmbServerConfiguration -EnableSMB1Protocol $false')
    
    print("Disabling SMBv2 and SMBv3...")
    run_powershell_command('Set-SmbServerConfiguration -EnableSMB2Protocol $false')

    # Alternatively, to completely disable SMB (all versions):
    # run_powershell_command('Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart')
    # run_powershell_command('Disable-WindowsOptionalFeature -Online -FeatureName SMB2Protocol -NoRestart')

if __name__ == "__main__":
    # Check for admin rights
    if not subprocess.run('net session', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        print("This script requires administrator privileges. Please run as administrator.")
        sys.exit(1)

    # Call the function to disable SMB
    disable_smb()
    print("SMB has been disabled successfully.")
