import subprocess
import sys

def delete_all_restore_points():
    """
    Deletes all system restore points on Windows using vssadmin.
    Requires administrator privileges.
    """
    if not sys.platform.startswith("win"):
        print("This function is only supported on Windows.")
        return False

    try:
        # The /for=c: argument can be changed for other drives if needed
        result = subprocess.run(
            ["vssadmin", "delete", "shadows", "/all", "/quiet"],
            capture_output=True, text=True, shell=True
        )
        if result.returncode == 0:
            print("All system restore points deleted successfully.")
            return True
        else:
            print("Failed to delete restore points.")
            print("Output:", result.stdout)
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print(f"Error deleting restore points: {e}")
        return False

if __name__ == "__main__":
    delete_all_restore_points()
