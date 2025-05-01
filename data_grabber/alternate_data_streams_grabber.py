import subprocess
import os

def find_alternate_data_streams(directory):
    """
    Returns a list of files with alternate data streams in the given directory (Windows only).
    """
    if not os.path.isdir(directory):
        return []
    ads_files = []
    try:
        output = subprocess.check_output(
            f'dir /r "{directory}"', shell=True, encoding='utf-8', errors='ignore'
        )
        for line in output.splitlines():
            if ':' in line and not line.strip().startswith('Directory of'):
                ads_files.append(line.strip())
    except Exception:
        pass
    return ads_files

if __name__ == "__main__":
    for line in find_alternate_data_streams(os.getcwd()):
        print(line)
