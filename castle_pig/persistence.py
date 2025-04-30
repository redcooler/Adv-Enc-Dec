import os
import sys

try:
    import winreg  # Only available on Windows
except ImportError:
    winreg = None

def add_registry_persistence(entry_name="CastlePigPersistence", script_path=None, python_exe=None):
    """
    Adds a registry key to HKCU\Software\Microsoft\Windows\CurrentVersion\Run
    to run this script at user logon.
    """
    if winreg is None:
        print("winreg module not available. This function only works on Windows.")
        return False

    if script_path is None:
        script_path = os.path.abspath(sys.argv[0])
    if python_exe is None:
        python_exe = sys.executable

    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = f'"{python_exe}" "{script_path}"'

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, entry_name, 0, winreg.REG_SZ, value)
        print(f"Registry persistence added: {entry_name} -> {value}")
        return True
    except Exception as e:
        print(f"Failed to add registry persistence: {e}")
        return False

def remove_registry_persistence(entry_name="CastlePigPersistence"):
    """
    Removes the registry key for persistence.
    """
    if winreg is None:
        print("winreg module not available. This function only works on Windows.")
        return False

    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, entry_name)
        print(f"Registry persistence removed: {entry_name}")
        return True
    except FileNotFoundError:
        print(f"No registry entry found for: {entry_name}")
        return False
    except Exception as e:
        print(f"Failed to remove registry persistence: {e}")
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add or remove Windows registry persistence (Run key).")
    parser.add_argument("action", choices=["add", "remove"], help="Add or remove persistence")
    parser.add_argument("--entry-name", default="CastlePigPersistence", help="Registry entry name")
    parser.add_argument("--script-path", default=None, help="Path to the script to run at logon")
    parser.add_argument("--python-exe", default=None, help="Path to the Python executable")
    args = parser.parse_args()

    if args.action == "add":
        add_registry_persistence(args.entry_name, args.script_path, args.python_exe)
    else:
        remove_registry_persistence(args.entry_name)
