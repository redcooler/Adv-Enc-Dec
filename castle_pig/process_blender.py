import sys
import os

def set_process_title_windows(title="explorer.exe"):
    """
    Sets the console window title to mimic a legitimate process.
    Only affects the window title, not the actual process name.
    """
    if os.name == "nt":
        os.system(f"title {title}")

def run_hidden_windows():
    """
    Relaunches the script with a hidden window (no console).
    Only works on Windows.
    """
    if os.name != "nt":
        print("Hidden mode is only supported on Windows.")
        return

    import subprocess

    # If already hidden, do nothing
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return

    # Relaunch with a hidden window
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0  # SW_HIDE

    subprocess.Popen([sys.executable] + sys.argv, startupinfo=si)
    sys.exit(0)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Blend process in as a legitimate Windows process.")
    parser.add_argument("--title", default="explorer.exe", help="Window title to set (default: explorer.exe)")
    parser.add_argument("--hidden", action="store_true", help="Run with hidden window (Windows only)")
    args = parser.parse_args()

    set_process_title_windows(args.title)
    if args.hidden:
        run_hidden_windows()
    print("Process is now blending in (window title set, optionally hidden).")
