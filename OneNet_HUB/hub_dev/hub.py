import subprocess
import time
import socket
import pygetwindow as gw
import pyautogui
import os

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Window size and center position
window_width = screen_width // 3
window_height = screen_height // 3
center_x = (screen_width - window_width) // 2
center_y = (screen_height - window_height) // 2

# Positions for surrounding windows
surrounding_positions = [
    (center_x - window_width, center_y - window_height),  # Top-left
    (center_x, center_y - window_height),                # Top-center
    (center_x + window_width, center_y - window_height), # Top-right
    (center_x - window_width, center_y),                 # Middle-left
    (center_x + window_width, center_y),                 # Middle-right
    (center_x - window_width, center_y + window_height), # Bottom-left
    (center_x, center_y + window_height),                # Bottom-center
    (center_x + window_width, center_y + window_height), # Bottom-right
]

def open_window(title, working_dir):
    """Opens a new Command Prompt window with a specified title and working directory."""
    print(f"Opening window with title: {title} in directory: {working_dir}")
    
    # Using os.path.join to properly join the path components
    node_script_path = os.path.join("d:", "OneNet", "node.py")
    
    print(f"Resolved node script path: {node_script_path}")  # Debug print for the path
    
    if not os.path.exists(node_script_path):
        print(f"Error: '{node_script_path}' does not exist.")
        return None
    
    # Start node.py with the correct path
    subprocess.Popen(
        f"start cmd /k title {title} & python \"{node_script_path}\" {title.split()[-1]}",
        cwd=working_dir,
        shell=True
    )
    time.sleep(2)  # Allow time for the window to open

    # Locate the window by its title
    for _ in range(10):
        windows = gw.getWindowsWithTitle(title)
        if windows:
            print(f"Found window: {windows[0]}")
            return windows[0]
        time.sleep(0.5)  # Retry if not found
    print(f"Error: Could not find window titled '{title}'")
    return None

def position_window(window, x, y):
    """Repositions and resizes a window."""
    try:
        window.moveTo(x, y)
        window.resizeTo(window_width, window_height)
        print(f"Window '{window.title}' positioned at ({x}, {y})")
    except Exception as e:
        print(f"Error positioning window {window.title}: {e}")

def send_command_to_node(node_id, command):
    """Sends a command to the specified node via its socket."""
    host = "127.0.0.1"
    port = 5000 + node_id
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)  # Timeout after 5 seconds
            client_socket.connect((host, port))
            client_socket.sendall(command.encode())
            response = client_socket.recv(1024).decode()
            print(f"[Hub] Response from Node {node_id}: {response}")
    except (ConnectionRefusedError, socket.error) as e:
        print(f"[Hub] Error communicating with Node {node_id}: {e}")

def main():
    base_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))  # Get parent directory of hub_dev

    # Step 1: Open the hub window
    hub_title = "Hub"
    hub_working_dir = os.path.join(base_dir, "hub_dev")
    hub_window = open_window(hub_title, hub_working_dir)
    if hub_window:
        position_window(hub_window, center_x, center_y)
    else:
        print("Error: Could not open the hub window.")
        return

    # Step 2: Open and position surrounding windows
    for i, (x, y) in enumerate(surrounding_positions, start=1):
        node_title = f"Node {i}"
        node_working_dir = os.path.join(base_dir, f"node_{i}")
        if not os.path.exists(node_working_dir):
            print(f"Error: Directory '{node_working_dir}' does not exist.")
            continue

        node_window = open_window(node_title, node_working_dir)
        if node_window:
            position_window(node_window, x, y)
            # Send test command to the node
            time.sleep(3)  # Allow node to initialize
            send_command_to_node(i, "initialize")  # Initialize node
        else:
            print(f"Error: Could not open window {node_title}.")

    # Step 3: Test communication with all nodes
    for i in range(1, len(surrounding_positions) + 1):
        send_command_to_node(i, "exec TestTask")  # Execute a task on each node

if __name__ == "__main__":
    main()
