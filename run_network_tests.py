"""
Standalone Runner for 06 - Network Testing
Executes offline simulation, 3G throttling, 500 server error handling, and recovery tests.
Usage: python tests/06_network_testing/run_network_tests.py
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(os.path.join(REPORT_DIR, "screenshots"), exist_ok=True)

REPORT_FILE = os.path.join(REPORT_DIR, "network_test_report.html")

def run():
    print("=" * 65)
    print(" [RUN] RUNNING 06 - NETWORK RESILIENCE AUTOMATION TESTS")
    print("=" * 65)

    cmd = [
        sys.executable, "-m", "pytest",
        SCRIPT_DIR,
        f"--html={REPORT_FILE}",
        "--self-contained-html",
        "-v"
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    ret = subprocess.run(cmd, cwd=PROJECT_ROOT, env=env)

    print("\n" + "=" * 65)
    if ret.returncode == 0:
        print(" [PASS] ALL NETWORK RESILIENCE SCENARIOS PASSED!")
    else:
        print(f" [FAIL] NETWORK TESTS FINISHED WITH EXIT CODE: {ret.returncode}")
    print(f" [*] HTML Execution Report: {REPORT_FILE}")
    print(f" [*] Screenshots saved in: {os.path.join(REPORT_DIR, 'screenshots')}")
    print("=" * 65)
    return ret.returncode

if __name__ == "__main__":
    sys.exit(run())
