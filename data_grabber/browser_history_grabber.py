import os
import shutil
import sqlite3

def get_chrome_history():
    """
    Returns a list of (url, title, last_visit_time) from Chrome's history.
    """
    local = os.getenv("LOCALAPPDATA")
    history_path = os.path.join(local, "Google", "Chrome", "User Data", "Default", "History")
    if not os.path.exists(history_path):
        return []
    tmp_db = os.path.join(os.getenv("TEMP"), "chrome_history.db")
    try:
        shutil.copy2(history_path, tmp_db)
        conn = sqlite3.connect(tmp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 50")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        os.remove(tmp_db)
        return results
    except Exception:
        return []

if __name__ == "__main__":
    for url, title, last_visit in get_chrome_history():
        print(f"{title} | {url} | {last_visit}")
