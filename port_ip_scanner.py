import socket
import ipinfo
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import os
from dotenv import load_dotenv  # NEW

# Load environment variables from .env file
load_dotenv()

# Retrieve the API token from the environment
API_TOKEN = os.getenv("IPINFO_API_TOKEN")  # UPDATED
ipinfo_handler = ipinfo.getHandler(API_TOKEN)
     
COMMON_PORTS = {
    7: "ECHO",                      # Echo test service
    13: "DAYTIME",                  # Returns current date and time
    19: "CHARGEN",                  # Character generator (often abused in DDoS)
    20: "FTP-DATA",                 # FTP data transfer
    21: "FTP",                      # File Transfer Protocol
    22: "SSH",                      # Secure Shell for remote login
    23: "Telnet",                   # Remote login (insecure)
    25: "SMTP",                     # Simple Mail Transfer Protocol
    37: "TIME",                     # Time protocol
    53: "DNS",                      # Domain Name System
    69: "TFTP",                     # Trivial File Transfer Protocol
    79: "FINGER",                   # User information lookup
    80: "HTTP",                     # Hypertext Transfer Protocol (web)
    110: "POP3",                    # Post Office Protocol v3
    111: "RPCBIND",                 # RPC port mapper
    113: "IDENT",                   # Identification protocol
    135: "MSRPC",                   # Microsoft RPC
    139: "NETBIOS-SSN",             # NetBIOS Session Service
    143: "IMAP",                    # Internet Message Access Protocol
    161: "SNMP",                    # Simple Network Management Protocol
    162: "SNMPTRAP",                # SNMP trap messages
    1723: "PPTP",                   # Point-to-Point Tunneling Protocol (VPN)
    389: "LDAP",                    # Lightweight Directory Access Protocol
    427: "SLP",                     # Service Location Protocol
    443: "HTTPS",                   # HTTP Secure (SSL/TLS)
    445: "MICROSOFT-DS",            # SMB over TCP (Windows shares)
    465: "SMTPS",                   # SMTP over SSL
    514: "SYSLOG",                  # System log protocol
    515: "LPD",                     # Line Printer Daemon
    546: "DHCPv6 Client",           # DHCP for IPv6 - client
    547: "DHCPv6 Server",           # DHCP for IPv6 - server
    554: "RTSP",                    # Real-Time Streaming Protocol
    587: "SMTP (Submission)",       # Mail submission agent
    5900: "VNC",                    # Virtual Network Computing
    593: "RPC over HTTP",           # Microsoft RPC via HTTP
    636: "LDAPS",                   # LDAP over SSL
    873: "RSYNC",                   # Remote file synchronization
    993: "IMAPS",                   # IMAP over SSL
    995: "POP3S",                   # POP3 over SSL
    1025: "NFS/DB-LISTENER",        # Windows RPC / Oracle DB
    1080: "SOCKS",                  # Proxy protocol
    1433: "MSSQL",                  # Microsoft SQL Server
    1434: "MSSQL Monitor",          # Microsoft SQL Monitor Service
    1521: "Oracle DB",              # Oracle Database
    1812: "RADIUS",                 # Remote Authentication Dial-In User Service
    1813: "RADIUS Accounting",      # RADIUS accounting service
    1900: "SSDP",                   # Simple Service Discovery Protocol (IoT)
    2000: "Cisco SCCP",             # Cisco IP Phones
    2048: "DFS",                    # Distributed File System
    2049: "NFS",                    # Network File System
    2483: "Oracle DB (TCP)",        # Oracle database over TCP
    2484: "Oracle DB (SSL)",        # Oracle database over SSL
    27017: "MongoDB",               # NoSQL database
    3268: "Global Catalog",         # Microsoft Active Directory
    3300: "SAP-R3",                 # SAP R/3 system
    3306: "MYSQL",                  # MySQL database
    3388: "CBServer",               # Sometimes used by backdoors
    3389: "RDP",                    # Remote Desktop Protocol
    3689: "DAAP",                   # iTunes music sharing
    5000: "UPnP / Flask",           # Universal Plug and Play / Flask dev server
    5060: "SIP",                    # Session Initiation Protocol (VoIP)
    5061: "SIPS",                   # SIP over TLS (secure)
    5432: "PostgreSQL",             # PostgreSQL database
    5431: "UPnP Hijack",            # Common UPnP vuln
    5800: "VNC over Web",           # Web-based VNC
    6379: "Redis",                  # In-memory data store
    6667: "IRC",                    # Internet Relay Chat
    7000: "AFS",                    # Andrew File System
    8080: "HTTP-PROXY",             # Common alt for HTTP
    8081: "HTTP-ALT",               # Alternate web interface
    8443: "HTTPS-ALT",              # Alternate HTTPS
    8888: "Alternate HTTP",         # Dev tools, proxy, testing
    9000: "SonarQube / php-fpm",    # Static analysis or PHP FastCGI
    9001: "Tor ORPort",             # Onion Routing (Tor)
    9100: "JetDirect Printing",     # Raw printing over TCP
    10000: "Webmin",                # Web-based system admin
    11211: "Memcached",             # Distributed memory caching
    27015: "Steam Games"            # Valve games server (e.g., CS, TF2)
}


# Global variable to control scanning
stop_scan = False

# Function to scan ports 
def scan_ports(ip):
    global stop_scan
    results = []
    total_ports = len(COMMON_PORTS)
    for index, (port, service) in enumerate(COMMON_PORTS.items()):
        if stop_scan:
            results.append("Scan stopped...")
            break
        progress_var.set((index + 1) / total_ports * 100)
        app.update_idletasks()  # Forces GUI update

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((ip, port))
                if result == 0:
                    result_text = f"Port {port} ({service}) is open"
                    if service in ["Telnet", "FTP"]:
                        result_text += " ⚠️ [WARNING: High Risk Service]"
                    results.append(result_text)
                else:
                    results.append(f"Port {port} ({service}) is closed")
        except Exception as e:
            results.append(f"Error scanning port {port}: {str(e)}")
    return results

# Function to get IP information 
def get_ip_info(ip):
    try:
        details = ipinfo_handler.getDetails(ip)
        info = [
            f"IP: {details.ip}",
            f"Hostname: {details.hostname}",
            f"City: {details.city}",
            f"Region: {details.region}",
            f"Country: {details.country_name}",
            f"Location (Lat, Long): {details.loc}",
            f"Organization: {details.org}",
            f"Postal Code: {details.postal}",
            f"Timezone: {details.timezone}"
        ]
        return info
    except Exception as e:
        return [f"Error fetching IP info: {str(e)}"]

# Function that runs when scan button is clicked 
def run_scan():
    global stop_scan
    stop_scan = False
    
    # Reset progress bar at start
    progress_var.set(0)
    app.update_idletasks()
    
    ip_or_hostname = ip_entry.get().strip()
    if not ip_or_hostname:
        messagebox.showerror("Input Error", "Please enter a valid IP address or hostname.")
        return

    output_box.delete(1.0, tk.END)

    try:
        ip = socket.gethostbyname(ip_or_hostname)
    except Exception as e:
        output_box.insert(tk.END, f"Error resolving hostname: {str(e)}\n")
        return

    output_box.insert(tk.END, f"Scanning IP: {ip}\n\n")

    #Port Scanning
    port_results = scan_ports(ip)
    for result in port_results:
        if "is open" in result:
            output_box.insert(tk.END, result + "\n", "open")
        elif "is closed" in result:
            output_box.insert(tk.END, result + "\n", "closed")
        else:
            output_box.insert(tk.END, result + "\n", "stopped")

    output_box.insert(tk.END, "\nFetching IP Information...\n\n")
    
    #IP Info 
    ip_info = get_ip_info(ip)
    output_box.insert(tk.END, "\n".join(ip_info))

# Threaded version of run_scan() 
def start_scan_thread():
    scan_thread = threading.Thread(target=run_scan)
    scan_thread.start()

# Stop button function 
def stop_scanning():
    global stop_scan
    stop_scan = True

# Save results to file 
def save_to_file():
    content = output_box.get(1.0, tk.END)
    if not content.strip():
        messagebox.showinfo("Info", "No results to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Results saved to {file_path}")

# Clear output
def clear_output():
    output_box.delete(1.0, tk.END)

# Copy to clipboard
def copy_to_clipboard():
    content = output_box.get(1.0, tk.END)
    app.clipboard_clear()
    app.clipboard_append(content)
    app.update()

# Auto-fill public IP
def autofill_my_ip():
    try:
        my_ip = requests.get('https://api.ipify.org').text
        ip_entry.delete(0, tk.END)
        ip_entry.insert(0, my_ip)
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch public IP: {str(e)}")

# GUI Setup
app = tk.Tk()
app.title("Port & IP Info Scanner - Enhanced Version")
app.geometry("750x650")

# Input Label and Entry 
ttk.Label(app, text="Enter IP Address or Hostname:").pack(pady=10)
ip_entry = ttk.Entry(app, width=50)
ip_entry.pack()

# Buttons Row 
frame_buttons = ttk.Frame(app)
frame_buttons.pack(pady=10)

ttk.Button(frame_buttons, text="Scan", command=start_scan_thread).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Stop", command=stop_scanning).grid(row=0, column=1, padx=5)
ttk.Button(frame_buttons, text="Clear", command=clear_output).grid(row=0, column=2, padx=5)
ttk.Button(frame_buttons, text="Save", command=save_to_file).grid(row=0, column=3, padx=5)
ttk.Button(frame_buttons, text="Copy", command=copy_to_clipboard).grid(row=0, column=4, padx=5)
ttk.Button(frame_buttons, text="Scan My IP", command=autofill_my_ip).grid(row=0, column=5, padx=5)

# Output Text Box
output_box = tk.Text(app, height=25, width=90)
output_box.pack(pady=10)

# Progress Bar Variable and Widget 
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(app, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, padx=20, pady=(5, 15))

# Add color tags
output_box.tag_configure("open", foreground="green")
output_box.tag_configure("closed", foreground="red")
output_box.tag_configure("stopped", foreground="orange")


# Start GUI loop
app.mainloop()
