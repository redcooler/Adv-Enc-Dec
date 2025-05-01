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
            continue
    return processes

if __name__ == "__main__":
    for proc in get_process_list():
        print(f"{proc['name']} (PID: {proc['pid']}, PPID: {proc['ppid']}, EXE: {proc['exe']})")
