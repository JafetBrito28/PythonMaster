import os
import socket
import hashlib
import subprocess
import time
from datetime import datetime

# Define the log file path
log_file_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'security_audit_log.txt')

# Welcome message and initial scan details
def create_welcome_file():
    with open(log_file_path, "w") as f:
        f.write("WELCOME TO YOUR FIRST SECURITY SCAN\n\n")
        f.write(f"Date and Time: {datetime.now()}\n")
        f.write("This script will perform a basic security check on your system.\n\n")
        f.write("Please be patient while the scan is in progress...\n\n")

# Port scanning function (same as before)
def scan_ports(target, start_port, end_port):
    open_ports = []
    port_descriptions = {
        # ... (Same extensive port descriptions from the previous response)
    }

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  # Set a timeout of 0.5 seconds to avoid blocking
                result = s.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    service_name, description = port_descriptions.get(port, ("Unknown", "Unknown service"))
                    risk = "Potentially risky" if port in [21, 23, 3389, 1723] else "Generally safe"
                    print(f"Port {port} open ({service_name}): {description} - {risk}")
        except socket.gaierror:
            print(f"Error: Could not resolve host '{target}'")
            return
        except:
            pass  # Ignore other errors (e.g., if the port is blocked)

    if not open_ports:
        print(f"No open ports found on {target} between {start_port} and {end_port}")
    return open_ports

# Basic malware scanning (using a simplified signature-based approach)
def scan_for_malware():
    malware_signatures = {
        "eicar_test_file": b"X5O!P%@AP[4\x50ZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
        # Add more signatures as needed (use bytes, not strings)
    }

    with open(log_file_path, "a") as f:
        f.write("\nMalware Scan Results:\n")
        for filename in os.listdir():
            try:
                with open(filename, "rb") as file:
                    content = file.read()
                    for name, signature in malware_signatures.items():
                        if signature in content:
                            f.write(f"WARNING: Potential malware detected in {filename} (Signature: {name})\n")
            except PermissionError:
                pass  # Ignore files that cannot be read

# Suspicious activity monitoring (simplified example)
def monitor_activity():
    last_modified_files = {}
    while True:
        for filename in os.listdir():
            try:
                modified_time = os.path.getmtime(filename)
                if filename not in last_modified_files:
                    last_modified_files[filename] = modified_time
                elif modified_time > last_modified_files[filename]:
                    with open(log_file_path, "a") as f:
                        f.write(f"WARNING: File {filename} was modified at {datetime.fromtimestamp(modified_time)}\n")
                    last_modified_files[filename] = modified_time
            except PermissionError:
                pass  # Ignore files that cannot be read
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    create_welcome_file()
    open_ports = scan_ports("localhost", 1, 1024)
    scan_for_malware()
    # monitor_activity()  # Uncomment to enable continuous activity monitoring
