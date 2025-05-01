# data_grabber/system_info_grabber.py

import os
import platform
import socket
import subprocess
import psutil
import requests
import getpass
from datetime import datetime, timedelta

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        return "Unavailable"

def get_windows_update_info():
    try:
        output = subprocess.check_output(
            'wmic qfe get HotFixID,InstalledOn', shell=True, encoding='utf-8', errors='ignore'
        )
        lines = [line.strip() for line in output.split('\n') if line.strip() and "HotFixID" not in line]
        if lines:
            last_update = lines[-1]
            return last_update
        return "Unavailable"
    except Exception:
        return "Unavailable"

def get_mac_addresses():
    macs = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                macs.append(addr.address)
    return macs

def get_uptime():
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        now = datetime.now()
        uptime = now - boot_time
        return str(uptime).split('.')[0]  # Remove microseconds
    except Exception:
        return "Unavailable"

def get_system_info():
    info = {}
    info['Username'] = getpass.getuser()
    info['Computer Name'] = platform.node()
    info['Local IP'] = socket.gethostbyname(socket.gethostname())
    info['Public IP'] = get_public_ip()
    info['Windows Version'] = platform.platform()
    info['Windows Release'] = platform.release()
    info['Windows Version Number'] = platform.version()
    info['System Architecture'] = platform.machine()
    info['Processor'] = platform.processor()
    info['RAM (GB)'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    info['CPU Cores'] = psutil.cpu_count(logical=True)
    info['Disk Total (GB)'] = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
    info['Disk Free (GB)'] = round(psutil.disk_usage('/').free / (1024 ** 3), 2)
    info['MAC Addresses'] = ', '.join(get_mac_addresses())
    info['Uptime'] = get_uptime()
    info['Last Windows Update'] = get_windows_update_info()
    return info

if __name__ == "__main__":
    info = get_system_info()
    for k, v in info.items():
        print(f"{k}: {v}")
