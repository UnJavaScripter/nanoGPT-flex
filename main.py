import paramiko
import socket
import os
import time
import http.server
import socketserver
import threading

# Constants
USERNAME = "your_username"  # Replace with the remote machine username
PASSWORD = "your_password"  # Replace with the password
PORT = 22  # Default SSH port

# Function to get the IP of the remote host
def get_remote_ip():
    # Replace with the command or method to get the remote host IP dynamically
    # For example, querying a cloud provider's API or using a hostname lookup
    return socket.gethostbyname('your_remote_host_hostname')  # Replace 'your_remote_host_hostname' with the appropriate hostname

# Function to connect via SSH and set the environment variable
def set_debian_frontend():
    try:
        # Get the dynamic IP of the host
        HOST = get_remote_ip()
        
        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote host
        print("Connecting to the remote host...")
        ssh_client.connect(HOST, PORT, USERNAME, PASSWORD)
        
        # Command to set DEBIAN_FRONTEND to 'web'
        command = "echo 'export DEBIAN_FRONTEND=web' >> ~/.bashrc"
        print(f"Running command: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Wait for command to complete and print any output/errors
        stdout.channel.recv_exit_status()
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Command to start a simple HTTP server
        command = "nohup python3 -m http.server 8080 &"
        print(f"Starting HTTP server: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        stdout.channel.recv_exit_status()
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print(f"Setup complete. You can access the remote host via: http://{HOST}:8080")
        
    except (paramiko.AuthenticationException, socket.error) as e:
        print(f"Connection failed: {e}")
    finally:
        # Close the SSH connection
        ssh_client.close()

if __name__ == "__main__":
    set_debian_frontend()
