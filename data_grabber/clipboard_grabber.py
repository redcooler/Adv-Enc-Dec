import subprocess
import sys

def get_clipboard():
    """
    Returns the current clipboard text (Windows only).
    """
    if sys.platform.startswith("win"):
        try:
            return subprocess.check_output('powershell Get-Clipboard', shell=True, encoding='utf-8', errors='ignore').strip()
        except Exception as e:
            return f"Error: {e}"
    else:
        return "Clipboard extraction only supported on Windows."

if __name__ == "__main__":
    print(get_clipboard())
