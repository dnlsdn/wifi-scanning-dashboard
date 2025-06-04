# sniffer.py
from scapy.all import *
import csv
import os

# Percorso assoluto al file CSV in modo da poter eseguire lo script
# da qualunque directory mantenendo l'output nello stesso path del sorgente
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "wifi_packets.csv")

# Se il CSV non esiste, crealo con l'header
if not os.path.isfile(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "MAC_Source", "BSSID", "SSID", "RSSI", "Channel"])

def packet_handler(pkt):
    if pkt.haslayer(Dot11):
        mac_src = pkt.addr2 if pkt.addr2 else ""
        bssid = pkt.addr3 if pkt.addr3 else ""
        ssid = ""
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            ssid = pkt.info.decode(errors="ignore")
        rssi = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else ""
        channel = pkt.Channel if hasattr(pkt, 'Channel') else ""
        timestamp = pkt.time
        with open(OUTPUT_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, mac_src, bssid, ssid, rssi, channel])

if __name__ == "__main__":
    print(f"[*] Avvio sniffing su wlan1mon: i dati andranno in {OUTPUT_FILE}")
    sniff(iface="wlan1mon", prn=packet_handler, store=False)
