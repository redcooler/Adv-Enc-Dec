# process_utils.py
import psutil

def get_process_list():
    """
    Returns a list of dicts with process info: name, pid, ppid, and exe path.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'exe']):
        try:
            info = proc.info
            processes.append(info)
        except Exception:
            # Handle potential exceptions (e.g., permission errors) gracefully
            continue
    return processes

def format_process_info(process_info):
    """
    Formats process information into a readable string.
    """
    return (
        f"{process_info.get('name', 'N/A')} "
        f"(PID: {process_info.get('pid', 'N/A')}, "
        f"PPID: {process_info.get('ppid', 'N/A')}, "
        f"EXE: {process_info.get('exe', 'N/A')})"
    )

+