# WiFi Scanning Dashboard

A simple Python/Flask application that sniffs nearby Wi-Fi 802.11 packets (using a Realtek AWUS036ACH USB adapter in monitor mode) and displays the last N captured packets in real time via a web dashboard.

## Project Structure

```
wifi-scanning-dashboard/
├── app.py               # Flask application
├── sniffer.py           # Scapy-based packet sniffer
├── templates/
│   └── index.html       # HTML template for the dashboard
├── venv/                # Python virtual environment (ignored by Git)
├── wifi_packets.csv     # Captured packet data (ignored by Git)
├── .gitignore
└── README.md
```

- **sniffer.py**
  Uses [Scapy](https://scapy.net/) to sniff 802.11 packets from the `wlan1mon` interface (AWUS036ACH in monitor mode).
  1. If `wifi_packets.csv` does not exist, it creates the file with a header row.
  2. For each 802.11 packet, it extracts:
     - `Timestamp` (epoch time)
     - `MAC_Source` (addr2)
     - `BSSID` (addr3)
     - `SSID` (for Beacon/ProbeResp frames)
     - `RSSI` (dBm)
     - `Channel`
  3. Appends each record as a new line in `wifi_packets.csv`.

- **app.py**
  A Flask web application that provides two routes:
  - `/data`: returns a JSON array containing the **last 50** rows from `wifi_packets.csv` (excluding the header).
  - `/`: serves `templates/index.html`.

- **templates/index.html**
  A basic HTML page with a `<table>` and a small JavaScript snippet that:
  1. Fetches `/data` every 2 seconds.
  2. Parses the JSON result and populates the table with:
     - Local time (converted from timestamp)
     - MAC source
     - BSSID
     - SSID
     - RSSI (dBm)
     - Channel/Frequency

## Prerequisites

- Python 3.x
- A Realtek AWUS036ACH USB Wi-Fi adapter supported by the `rtw88` driver
- `aircrack-ng` installed (for `airmon-ng`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YourUsername/wifi-scanning-dashboard.git
   cd wifi-scanning-dashboard
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install scapy flask
   ```

## How to Use

### 1. Enable Monitor Mode on the AWUS036ACH

In a separate terminal, run:
```bash
cd ~/projects/common/tools
./monitor.sh wlan1 start
```
This will spawn `wlan1mon` in monitor mode. Verify with:
```bash
iwconfig
```
You should see something like:
```
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
```

### 2. Run the Sniffer (requires root)

In the project root (with `venv` activated), run:
```bash
sudo ./venv/bin/python3 sniffer.py
```
This will start appending captured packet data to `wifi_packets.csv`. You can confirm by running in another terminal:
```bash
tail -f wifi_packets.csv
```

### 3. Run the Flask Dashboard

In a separate terminal (with `venv` still activated), run:
```bash
python3 app.py
```
Flask will start listening on `0.0.0.0:5000`. Open a browser (on any device in the same network) and navigate to:
```
http://<RASPBERRY_PI_IP>:5000/
```
The dashboard will show a table updating every 2 seconds with the latest sniffed packets.

### 4. Stop Everything

- To stop sniffing: press `Ctrl+C` in the terminal running `sniffer.py`.  
- To stop Flask: press `Ctrl+C` in the terminal running `app.py`.  
- To disable monitor mode:
  ```bash
  cd ~/projects/common/tools
  ./monitor.sh wlan1 stop
  ```

## Notes

- The `venv/` folder and `wifi_packets.csv` are ignored by Git via `.gitignore`.  
- If you prefer to run `sniffer.py` without `sudo`, you can assign Linux capabilities to the Python binary:
  ```bash
  sudo setcap cap_net_raw,cap_net_admin+eip /home/pi/projects/lvl1_recon/wifi_spy/venv/bin/python3
  ```
  After this, you may run:
  ```bash
  python3 sniffer.py
  ```
  as a normal user (inside the virtual environment).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
