"""
Standalone Runner for 02 - Responsive Testing
Executes responsive tests across Mobile, Tablet, Laptop, and Desktop viewports.
Usage: python tests/02_responsive_testing/run_responsive_tests.py
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

REPORT_FILE = os.path.join(REPORT_DIR, "responsive_test_report.html")

def run():
    print("=" * 65)
    print(" [RUN] RUNNING 02 - RESPONSIVE AUTOMATION TESTS (PLAYWRIGHT)")
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
        print(" [PASS] RESPONSIVE TESTS PASSED ACROSS ALL 5 VIEWPORTS!")
    else:
        print(f" [FAIL] RESPONSIVE TESTS FAILED WITH EXIT CODE: {ret.returncode}")
    print(f" [*] HTML Execution Report: {REPORT_FILE}")
    print(f" [*] Viewport Screenshots: {os.path.join(REPORT_DIR, 'screenshots')}")
    print("=" * 65)
    return ret.returncode

if __name__ == "__main__":
    sys.exit(run())
