"""
Standalone Runner for 01 - UI Testing
Executes all UI test cases and generates an HTML report and screenshots.
Usage: python tests/01_ui_testing/run_ui_tests.py
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

REPORT_FILE = os.path.join(REPORT_DIR, "ui_test_report.html")

def run():
    print("=" * 65)
    print(" [RUN] RUNNING 01 - UI AUTOMATION TESTS (PLAYWRIGHT + PYTEST)")
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
        print(" [PASS] UI TESTS COMPLETED SUCCESSFULLY!")
    else:
        print(f" [FAIL] UI TESTS FINISHED WITH EXIT CODE: {ret.returncode}")
    print(f" [*] HTML Execution Report: {REPORT_FILE}")
    print(f" [*] Screenshots saved to: {os.path.join(REPORT_DIR, 'screenshots')}")
    print("=" * 65)
    return ret.returncode

if __name__ == "__main__":
    sys.exit(run())
