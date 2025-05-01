import os

def get_rdp_connections():
    """
    Returns a list of RDP connection history from the registry (Windows only).
    """
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Terminal Server Client\Servers")
        servers = []
        i = 0
        while True:
            try:
                server = winreg.EnumKey(key, i)
                servers.append(server)
                i += 1
            except OSError:
                break
        return servers
    except Exception as e:
        return [f"Error: {e}"]

if __name__ == "__main__":
    for server in get_rdp_connections():
        print(server)
