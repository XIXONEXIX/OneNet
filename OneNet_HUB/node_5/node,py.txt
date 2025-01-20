import socket
import threading
import os
import sys

def handle_command(command, client_socket):
    """
    Processes received commands and sends a response to the client.

    Args:
        command (str): The command received from the client.
        client_socket (socket): The client socket to send the response back.
    """
    print(f"[Node] Received command: {command}")

    # Handle specific commands
    if command == "initialize":
        response = "Node initialized successfully."
        print(response)
    elif command.startswith("exec"):
        # Extract task details
        task = command.split(" ", 1)[1] if " " in command else "No task specified"
        response = f"Executing task: {task}"
        print(response)
    elif command == "status":
        # Example additional command
        response = "Node is running and ready."
        print(response)
    else:
        response = f"Unknown command: {command}"
        print(response)

    # Send the response back to the client
    try:
        client_socket.sendall(response.encode())
    except Exception as e:
        print(f"[Node] Error sending response: {e}")


def client_handler(client_socket, client_address):
    """
    Handles a single client connection.

    Args:
        client_socket (socket): The client's socket connection.
        client_address (tuple): The client's address (IP, port).
    """
    print(f"[Node] Connection established with {client_address}")
    try:
        while True:
            # Receive data from the client
            command = client_socket.recv(1024).decode()
            if command:
                handle_command(command, client_socket)
            else:
                print(f"[Node] Connection closed by {client_address}")
                break
    except ConnectionResetError:
        print(f"[Node] Connection reset by {client_address}")
    except Exception as e:
        print(f"[Node] Unexpected error with {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[Node] Connection with {client_address} has been terminated.")


def start_node_server(node_id):
    """
    Starts the node server to listen for incoming connections.

    Args:
        node_id (int): The unique ID of the node, used to determine its port.
    """
    host = "127.0.0.1"
    port = 5000 + node_id  # Assign a unique port based on the node ID

    # Create and configure the server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind((host, port))
            server_socket.listen(5)
            print(f"[Node {node_id}] Listening on {host}:{port}...")

            while True:
                # Accept new client connections
                client_socket, client_address = server_socket.accept()
                print(f"[Node {node_id}] New connection from {client_address}")
                # Start a new thread to handle the client
                threading.Thread(
                    target=client_handler, 
                    args=(client_socket, client_address), 
                    daemon=True
                ).start()
        except OSError as e:
            print(f"[Node {node_id}] Server error: {e}")
        except KeyboardInterrupt:
            print(f"[Node {node_id}] Shutting down server...")
        finally:
            print(f"[Node {node_id}] Server socket closed.")


def main():
    """
    Main function to start the node server.
    """
    # Validate command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python node.py <node_id>")
        sys.exit(1)

    # Parse and validate node ID
    try:
        node_id = int(sys.argv[1])
        if node_id < 0 or node_id > 100:  # Arbitrary range for validation
            raise ValueError("Node ID must be between 0 and 100.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Print node details
    print(f"[Node {node_id}] Starting...")
    print(f"[Node {node_id}] Current working directory: {os.getcwd()}")

    # Start the server
    start_node_server(node_id)


if __name__ == "__main__":
    main()
