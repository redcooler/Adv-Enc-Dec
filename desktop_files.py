import os

def get_all_files_from_desktop():
    """
    Recursively return a list of all file paths on the user's Desktop,
    including files in subfolders.
    """
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    files = []
    for root, dirs, filenames in os.walk(desktop):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

# Optional: CLI usage example
if __name__ == "__main__":
    files = get_all_files_from_desktop()
    for f in files:
        print(f)
