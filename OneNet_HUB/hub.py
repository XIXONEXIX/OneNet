import subprocess
import time
import pygetwindow as gw
import pyautogui

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

def open_window(title):
    """Opens a new Command Prompt window with a specified title."""
    print(f"Opening window with title: {title}")
    subprocess.Popen(f"start cmd /k title {title}", shell=True)
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

def main():
    # Step 1: Open the hub window
    hub_title = "Hub"
    hub_window = open_window(hub_title)
    if hub_window:
        position_window(hub_window, center_x, center_y)
    else:
        print("Error: Could not open the hub window.")
        return

    # Step 2: Open and position surrounding windows
    for i, (x, y) in enumerate(surrounding_positions, start=1):
        node_title = f"Node {i}"
        node_window = open_window(node_title)
        if node_window:
            position_window(node_window, x, y)
        else:
            print(f"Error: Could not open window {node_title}.")

if __name__ == "__main__":
    main()