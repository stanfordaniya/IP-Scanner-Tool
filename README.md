
## Port & IP Info Scanner by Aniya Stanford

## Description
This Python-based GUI application allows users to scan IP addresses or hostnames for open TCP ports and retrieve threat intelligence data using the IPInfo.io API. The application identifies over 80 commonly used ports (including Telnet, FTP, SSH, and RPC), providing real-time insight into open and closed ports, as well as metadata such as ASN, ISP organization, geolocation, and timezone.

> ⚠️ This application uses the IPInfo.io API. You must sign up at [ipinfo.io](https://ipinfo.io/signup) to retrieve a free API token. This token is required to run the scanner.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Planned Enhancements](#planned-enhancements)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/stanfordaniya/Port-IP-Info-Scanner.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Port-IP-Info-Scanner
   ```

3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your IPinfo API token:
   ```
   IPINFO_API_TOKEN=your_token_here
   ```

5. Run the application:
   ```bash
   python netscanner.py
   ```

## Usage

Once launched, the scanner allows you to:

1. **Enter an IP Address or Hostname**  
   Use the input field to specify the target address.

2. **Scan Ports**  
   Click the **Scan** button to perform a live scan of over 80 well-known TCP ports.

3. **View Threat Intelligence**  
   IPInfo.io enriches your scan results with metadata about the IP address, including:
   - ASN and ISP
   - City, Region, and Country
   - Postal code and Timezone
   - Organization

4. **Interact with the Results**  
   - Results are color-coded:
     - ✅ Green: Port is open  
     - ❌ Red: Port is closed  
     - 🟧 Orange: Scan manually stopped
   - Use action buttons to:
     - Stop the scan
     - Save output to a `.txt` file
     - Copy results to clipboard
     - Auto-fill your own public IP address

## Features

- 🧠 IP Intelligence with IPInfo API
- 🎨 Real-time output with color-coded scan results
- 📈 Progress bar for live scan feedback
- 🧵 Threaded scanning to prevent UI freeze
- 💾 Save & export scan results
- 🔍 Auto-fetch public IP address

## Planned Enhancements

- ✅ Customizable port range scanning
- ✅ Export to CSV or JSON
- ✅ Improved input validation and error handling
- ✅ Batch IP scanning support using IPInfo’s batch API
- ✅ Lightweight logging and analytics


