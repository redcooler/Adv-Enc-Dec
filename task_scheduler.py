"""
task_scheduler.py

Module to add a Python script to Windows Task Scheduler to run at logon.
"""

import os
import sys
import subprocess

def add_to_task_scheduler(
    task_name="MyPythonScriptAutoStart",
    script_path=None,
    python_exe=None,
    run_level="HIGHEST"
):
    """
    Adds the current script (or a specified script) to Windows Task Scheduler to run at logon.

    Args:
        task_name (str): Name for the scheduled task.
        script_path (str): Path to the script to run. Defaults to the current script.
        python_exe (str): Path to the Python executable. Defaults to the current Python interpreter.
        run_level (str): "LIMITED" or "HIGHEST" privileges.
    """

    if os.name != "nt":
        print("Task Scheduler integration is only supported on Windows.")
        return False

    if script_path is None:
        script_path = os.path.abspath(sys.argv[0])
    if python_exe is None:
        python_exe = sys.executable

    cmd = [
        "schtasks",
        "/Create",
        "/SC", "ONLOGON",
        "/TN", task_name,
        "/TR", f'"{python_exe}" "{script_path}"',
        "/RL", run_level,
        "/F"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Task '{task_name}' successfully added to Task Scheduler.")
            return True
        else:
            print(f"Failed to add task '{task_name}'. Error:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Add this or another Python script to Windows Task Scheduler (on logon)."
    )
    parser.add_argument(
        "--task-name", default="MyPythonScriptAutoStart",
        help="Name for the scheduled task"
    )
    parser.add_argument(
        "--script-path", default=None,
        help="Path to the script to run (default: this script)"
    )
    parser.add_argument(
        "--python-exe", default=None,
        help="Path to the Python executable (default: current interpreter)"
    )
    parser.add_argument(
        "--run-level", default="LIMITED", choices=["LIMITED", "HIGHEST"],
        help="Run level for the task (LIMITED or HIGHEST)"
    )

    args = parser.parse_args()
    add_to_task_scheduler(
        task_name=args.task_name,
        script_path=args.script_path,
        python_exe=args.python_exe,
        run_level=args.run_level
    )
