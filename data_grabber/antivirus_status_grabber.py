import subprocess
import sys

def get_antivirus_status():
    """
    Returns a list of installed antivirus products and their status (Windows only).
    """
    if not sys.platform.startswith("win"):
        return ["Antivirus status only supported on Windows."]
    try:
        output = subprocess.check_output(
            'powershell "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select displayName,productState"',
            shell=True, encoding='utf-8', errors='ignore'
        )
        return output.strip().split('\n')
    except Exception as e:
        return [f"Error: {e}"]

if __name__ == "__main__":
    for line in get_antivirus_status():
        print(line)
