import socket

def scan_ports(target, start_port, end_port):
    open_ports = []
    port_descriptions = {
        # Well-Known Ports (0-1023)
        7: ("Echo", "Echoes data back to the sender. Used for testing and debugging."),
        9: ("Discard", "Discards any data sent to it. Used for testing and debugging."),
        13: ("Daytime", "Provides the current date and time. Used for time synchronization."),
        17: ("QOTD", "Quote of the Day. Provides a random quote."),
        19: ("Chargen", "Generates characters. Used for testing and debugging."),
        20: ("FTP-Data", "File Transfer Protocol Data. Used for transferring files over FTP."),
        21: ("FTP", "File Transfer Protocol. Often used for file sharing, but can be insecure."),
        22: ("SSH", "Secure Shell. Used for secure remote access, generally safe if configured properly."),
        23: ("Telnet", "Unencrypted remote access. Highly insecure, avoid using."),
        25: ("SMTP", "Simple Mail Transfer Protocol. Used for sending emails."),
        53: ("DNS", "Domain Name System. Translates domain names to IP addresses."),
        67: ("DHCP", "Dynamic Host Configuration Protocol. Assigns IP addresses to devices on a network."),
        68: ("DHCP", "Dynamic Host Configuration Protocol. Used by clients to request IP addresses."),
        69: ("TFTP", "Trivial File Transfer Protocol. A simplified file transfer protocol, often used for booting devices."),
        80: ("HTTP", "Hypertext Transfer Protocol. Used for unencrypted web traffic."),
        110: ("POP3", "Post Office Protocol version 3. Used for receiving emails."),
        111: ("RPCbind", "Remote Procedure Call Bind. Maps RPC program numbers to transport addresses."),
        119: ("NNTP", "Network News Transfer Protocol. Used for reading and posting to Usenet newsgroups."),
        123: ("NTP", "Network Time Protocol. Synchronizes clocks over a network."),
        135: ("RPC", "Remote Procedure Call. Used for Microsoft RPC services."),
        137: ("NetBIOS-NS", "NetBIOS Name Service. Used for name resolution on Windows networks."),
        138: ("NetBIOS-DGM", "NetBIOS Datagram Service. Used for datagram communication on Windows networks."),
        139: ("NetBIOS-SSN", "NetBIOS Session Service. Used for session-oriented communication on Windows networks."),
        143: ("IMAP", "Internet Message Access Protocol. Used for accessing emails on a server."),
        161: ("SNMP", "Simple Network Management Protocol. Used for managing network devices."),
        162: ("SNMP-Trap", "SNMP Trap. Used for sending SNMP alerts."),
        179: ("BGP", "Border Gateway Protocol. Used for exchanging routing information between autonomous systems."),
        194: ("IRC", "Internet Relay Chat. Used for real-time text-based communication."),
        389: ("LDAP", "Lightweight Directory Access Protocol. Used for accessing directory services."),
        443: ("HTTPS", "Hypertext Transfer Protocol Secure. Used for encrypted web traffic, generally safe."),
        445: ("SMB", "Server Message Block. Used for file and printer sharing on Windows networks."),
        514: ("Syslog", "Syslog. Used for logging system messages."),
        515: ("LPD", "Line Printer Daemon. Used for printing."),
        993: ("IMAPS", "Internet Message Access Protocol over SSL/TLS. Encrypted version of IMAP."),
        995: ("POP3S", "Post Office Protocol version 3 over SSL/TLS. Encrypted version of POP3."),
        # Registered Ports (1024-49151)
        1433: ("MS-SQL-Server", "Microsoft SQL Server. Database server."),
        1521: ("Oracle", "Oracle database listener."),
        1723: ("PPTP", "Point-to-Point Tunneling Protocol. Used for creating VPNs, but considered insecure."),
        3306: ("MySQL", "MySQL database server."),
        3389: ("RDP", "Remote Desktop Protocol. Used for remote access to Windows systems, can be a target for attacks."),
        5432: ("PostgreSQL", "PostgreSQL database server."),
        5900: ("VNC", "Virtual Network Computing. Used for remote desktop access."),
        8080: ("HTTP-Proxy", "HTTP Proxy. Often used for web caches or anonymizing services."),
        # Dynamic and/or Private Ports (49152-65535)
        # These ports are often used by applications and services dynamically.
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

# Example usage:
target = "www.example.com"  # Replace with the host you want to scan
start_port = 1
end_port = 100
open_ports = scan_ports(target, start_port, end_port)

print("Open ports found:", open_ports)  # Display the open ports in a list
