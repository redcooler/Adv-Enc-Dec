import subprocess

def get_wifi_network_history():
    """
    Returns a list of all Wi-Fi profiles the system has ever connected to (Windows only).
    """
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'],
            encoding='utf-8', errors='ignore'
        )
        profiles = [line.split(":")[1].strip() for line in output.split('\n') if "All User Profile" in line]
        return profiles
    except Exception as e:
        return [f"Error: {e}"]

if __name__ == "__main__":
    for ssid in get_wifi_network_history():
        print(ssid)
