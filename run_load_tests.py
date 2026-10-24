"""
Standalone Runner for 03 - Load Testing (Locust)
Simulates concurrent virtual shoppers, measures RPS, response times, and failure rates.
Generates an HTML execution report in reports/load_test_report.html.
Usage: python tests/03_load_testing/run_load_tests.py
"""

import os
import sys
import time
import threading
import subprocess
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

REPORT_FILE = os.path.join(REPORT_DIR, "load_test_report.html")
CSV_PREFIX = os.path.join(REPORT_DIR, "load_stats")
LOCUST_FILE = os.path.join(SCRIPT_DIR, "locustfile.py")
BASE_URL = "http://127.0.0.1:8000"


def ensure_server_running():
    """Verify backend server is accessible; if not, spin up server in background."""
    try:
        res = requests.get(f"{BASE_URL}/api/health", timeout=1.0)
        if res.status_code == 200:
            return None
    except Exception:
        pass

    sys.path.insert(0, PROJECT_ROOT)
    import server
    from werkzeug.serving import make_server

    srv = make_server("127.0.0.1", 8000, server.app, threaded=True)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    time.sleep(1.0)
    return srv


def run():
    print("=" * 65)
    print(" [RUN] RUNNING 03 - LOAD AUTOMATION TESTING (LOCUST)")
    print("=" * 65)
    print(f" Target: {BASE_URL}")
    print(" Virtual Users: 20 | Spawn Rate: 5 users/sec | Duration: 15s")
    print("-" * 65)

    srv = ensure_server_running()

    cmd = [
        sys.executable, "-m", "locust",
        "-f", LOCUST_FILE,
        "--host", BASE_URL,
        "--headless",
        "-u", "20",
        "-r", "5",
        "--run-time", "15s",
        f"--html={REPORT_FILE}",
        f"--csv={CSV_PREFIX}"
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    ret = subprocess.run(cmd, cwd=PROJECT_ROOT, env=env)

    print("\n" + "=" * 65)
    if ret.returncode == 0:
        print(" [PASS] LOAD TESTING COMPLETED SUCCESSFULLY WITH 0 FAILURES!")
    else:
        print(f" [WARN] LOAD TEST FINISHED WITH EXIT CODE: {ret.returncode}")
    print(f" [*] Full Interactive HTML Report: {REPORT_FILE}")
    print(f" [*] CSV Performance Logs: {CSV_PREFIX}_stats.csv")
    print("=" * 65)

    if srv:
        srv.shutdown()

    return ret.returncode


if __name__ == "__main__":
    sys.exit(run())
