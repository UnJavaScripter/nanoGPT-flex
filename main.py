import paramiko
import socket
import os
import time
import http.server
import socketserver
import threading
import subprocess

# Constants
USERNAME = "your_username"  # Replace with the remote machine username
PASSWORD = "your_password"  # Replace with the password
PORT = 22  # Default SSH port

# Function to get the IP of the remote host using system tools
def get_remote_ip():
    try:
        # Using a system command to determine the IP address dynamically
        ip_command = "hostname -I"
        result = subprocess.run(ip_command, shell=True, capture_output=True, text=True)
        ip = result.stdout.strip().split()[0]  # Assuming the first IP is the correct one
        return ip
    except Exception as e:
        print(f"Failed to get the IP address: {e}")
        return None

# Function to connect via SSH and set the environment variable
def set_debian_frontend():
    try:
        # Get the dynamic IP of the host
        HOST = get_remote_ip()
        if not HOST:
            print("Unable to determine the IP address.")
            return
        
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
        
        # Wait for 5 minutes before closing the SSH connection
        print("Waiting for 5 minutes before closing the connection...")
        time.sleep(300)
        
    except (paramiko.AuthenticationException, socket.error) as e:
        print(f"Connection failed: {e}")
    finally:
        # Close the SSH connection
        ssh_client.close()
        print("SSH connection closed.")
        exit(0)

if __name__ == "__main__":
    set_debian_frontend()
