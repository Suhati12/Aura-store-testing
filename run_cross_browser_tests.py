"""
Standalone Runner for 05 - Cross-Browser Testing
Executes full user journeys across Chrome (Chromium), Firefox, and Microsoft Edge.
Usage: python tests/05_cross_browser_testing/run_cross_browser_tests.py
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

REPORT_FILE = os.path.join(REPORT_DIR, "cross_browser_test_report.html")

def run():
    print("=" * 65)
    print(" [RUN] RUNNING 05 - CROSS-BROWSER TESTING (CHROME, FIREFOX, EDGE)")
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
        print(" [PASS] CROSS-BROWSER TESTS PASSED ON CHROME, FIREFOX, AND EDGE!")
    else:
        print(f" [FAIL] CROSS-BROWSER TESTS FINISHED WITH EXIT CODE: {ret.returncode}")
    print(f" [*] HTML Execution Report: {REPORT_FILE}")
    print(f" [*] Screenshots saved in: {os.path.join(REPORT_DIR, 'screenshots')}")
    print("=" * 65)
    return ret.returncode

if __name__ == "__main__":
    sys.exit(run())
