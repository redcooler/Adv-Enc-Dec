import os
import glob
import datetime
import platform
import re

def get_application_usage_history(limit=None):
    """
    Extracts a simplified application usage history from Windows Prefetch files.

    This function lists executables for which Prefetch files exist and
    provides the last modified timestamp of the Prefetch file as an
    approximation of the application's last significant activity.

    Note:
    - This is Windows-specific.
    - Access to C:\\Windows\\Prefetch might require administrator privileges.
    - The last modified time of the .pf file is an approximation.
      Full Prefetch parsing provides more accurate last run times.

    Args:
        limit (int, optional): Maximum number of entries to return,
                               sorted by most recent. Defaults to None (all).

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              {'executable_name': str, 'last_activity_approx': datetime_object}
              Returns an empty list if not on Windows, Prefetch dir not found,
              or no .pf files are found.
              Returns a list with an error message dict if an error occurs.
    """
    if platform.system() != "Windows":
        return [{"error": "This function is Windows-specific."}]

    prefetch_dir = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Prefetch")

    if not os.path.isdir(prefetch_dir):
        return [{"error": f"Prefetch directory not found: {prefetch_dir}"}]

    app_usage = []
    try:
        # Regex to extract the executable name (e.g., NOTEPAD.EXE from NOTEPAD.EXE-C0FFEE12.pf)
        # It looks for a sequence of characters ending in .EXE (case-insensitive)
        # followed by a hyphen, 8 hex characters, and .pf
        exe_pattern = re.compile(r"^(.*\.EXE)-[0-9A-F]{8}\.pf$", re.IGNORECASE)

        for pf_file_path in glob.glob(os.path.join(prefetch_dir, "*.pf")):
            filename = os.path.basename(pf_file_path)
            match = exe_pattern.match(filename)

            if match:
                executable_name = match.group(1).upper() # Get the part before the hash
                try:
                    mtime_timestamp = os.path.getmtime(pf_file_path)
                    last_activity = datetime.datetime.fromtimestamp(mtime_timestamp)
                    app_usage.append({
                        "executable_name": executable_name,
                        "last_activity_approx": last_activity,
                    })
                except Exception as e_time:
                    # Could log this error if a logging system is in place
                    print(f"Warning: Could not get mtime for {pf_file_path}: {e_time}")
                    continue
            # else:
                # Optional: log files that didn't match the expected .EXE-HASH.pf pattern
                # print(f"Debug: Skipped non-standard prefetch filename: {filename}")


    except PermissionError:
        return [{
            "error": f"Permission denied accessing {prefetch_dir}. Try running as administrator."
        }]
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {e}"}]

    # Sort by last activity, most recent first
    app_usage.sort(key=lambda x: x.get("last_activity_approx", datetime.datetime.min), reverse=True)

    if limit and isinstance(limit, int) and limit > 0:
        return app_usage[:limit]

    return app_usage

if __name__ == "__main__":
    print("Attempting to extract application usage history (Windows Prefetch)...\n")
    usage_data = get_application_usage_history(limit=10)

    if usage_data and "error" in usage_data[0]:
        print(f"Error: {usage_data[0]['error']}")
    elif not usage_data:
        print("No application usage data found or an issue occurred.")
    else:
        print(f"{'Executable Name':<50} {'Last Activity (Approx.)'}")
        print(f"{'-'*50} {'-'*25}")
        for entry in usage_data:
            exe_name = entry.get("executable_name", "N/A")
            activity_time = entry.get("last_activity_approx", "N/A")
            if isinstance(activity_time, datetime.datetime):
                activity_time_str = activity_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                activity_time_str = str(activity_time)
            print(f"{exe_name:<50} {activity_time_str}")

    print("\nNote: Access to C:\\Windows\\Prefetch might require administrator privileges.")
