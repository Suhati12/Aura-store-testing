"""
Master Automation Test Suite Runner for Aura Luxe Store
Orchestrates and executes all 7 testing disciplines:
1. UI Testing
2. Responsive Testing
3. Load Testing
4. Performance Testing
5. Cross-Browser Testing
6. Network Resilience Testing
7. REST API Testing

Generates unified executive report at reports/master_test_report.html.
Usage: python tests/run_all_tests.py
"""

import os
import sys
import time
import subprocess
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(os.path.join(REPORT_DIR, "screenshots"), exist_ok=True)

MASTER_REPORT = os.path.join(REPORT_DIR, "master_test_report.html")

TEST_SUITES = [
    {
        "id": "01_ui",
        "title": "UI Testing",
        "description": "Navigation, search, product cards, buttons, forms, and cart flow",
        "runner": os.path.join(SCRIPT_DIR, "01_ui_testing", "run_ui_tests.py"),
        "report": "ui_test_report.html"
    },
    {
        "id": "02_responsive",
        "title": "Responsive Testing",
        "description": "Mobile, Tablet, Laptop, and Desktop viewports without overflow",
        "runner": os.path.join(SCRIPT_DIR, "02_responsive_testing", "run_responsive_tests.py"),
        "report": "responsive_test_report.html"
    },
    {
        "id": "03_load",
        "title": "Load Testing",
        "description": "Multi-user concurrent load simulation via Locust",
        "runner": os.path.join(SCRIPT_DIR, "03_load_testing", "run_load_tests.py"),
        "report": "load_test_report.html"
    },
    {
        "id": "04_performance",
        "title": "Performance Testing",
        "description": "Page load speed, TTFB, DOM Content Loaded, FCP, and Core Web Vitals",
        "runner": os.path.join(SCRIPT_DIR, "04_performance_testing", "run_performance_tests.py"),
        "report": "performance_report.html"
    },
    {
        "id": "05_cross_browser",
        "title": "Cross-Browser Testing",
        "description": "Automated verification across Chrome, Firefox, and Microsoft Edge",
        "runner": os.path.join(SCRIPT_DIR, "05_cross_browser_testing", "run_cross_browser_tests.py"),
        "report": "cross_browser_test_report.html"
    },
    {
        "id": "06_network",
        "title": "Network Testing",
        "description": "Slow internet (3G), offline mode, HTTP 500 error handling, and recovery",
        "runner": os.path.join(SCRIPT_DIR, "06_network_testing", "run_network_tests.py"),
        "report": "network_test_report.html"
    },
    {
        "id": "07_api",
        "title": "API Testing",
        "description": "REST endpoints positive and negative testing with pytest and requests",
        "runner": os.path.join(SCRIPT_DIR, "07_api_testing", "run_api_tests.py"),
        "report": "api_test_report.html"
    }
]


def generate_master_html_report(results, total_duration):
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count
    pass_rate = round((passed_count / len(results)) * 100, 1) if results else 0

    rows_html = ""
    for r in results:
        status_badge = '<span class="badge pass">PASSED [OK]</span>' if r["passed"] else '<span class="badge fail">FAILED [X]</span>'
        rows_html += f"""
        <tr>
          <td><strong>{r['title']}</strong><br><small style="color:#8C847C;">{r['description']}</small></td>
          <td>{r['duration']:.2f}s</td>
          <td>{status_badge}</td>
          <td><a href="{r['report']}" class="report-link" target="_blank">View Report &nearr;</a></td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Aura Luxe Store - Master Automation Testing Report</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #FAF8F5; color: #1E1B18; padding: 2.5rem 1rem; margin: 0; }}
    .container {{ max-width: 1000px; margin: 0 auto; background: #FFFFFF; padding: 3rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); }}
    .header {{ border-bottom: 1px solid #EBE5DF; padding-bottom: 1.5rem; margin-bottom: 2rem; }}
    h1 {{ font-size: 2.2rem; margin: 0 0 0.5rem 0; color: #1E1B18; }}
    .brand {{ color: #C88A83; font-style: italic; }}
    .meta {{ font-size: 0.95rem; color: #8C847C; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 2.5rem; }}
    .stat-card {{ background: #F4EFEA; padding: 1.5rem; border-radius: 12px; text-align: center; }}
    .stat-val {{ font-size: 2.2rem; font-weight: 700; color: #1E1B18; }}
    .stat-val.pass {{ color: #2e7d32; }}
    .stat-val.fail {{ color: #c62828; }}
    .stat-label {{ font-size: 0.85rem; text-transform: uppercase; color: #8C847C; margin-top: 0.3rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ padding: 1.1rem; text-align: left; border-bottom: 1px solid #EBE5DF; }}
    th {{ background: #FAF8F5; font-size: 0.9rem; text-transform: uppercase; color: #8C847C; }}
    .badge {{ padding: 0.35rem 0.8rem; border-radius: 9999px; font-size: 0.82rem; font-weight: 700; display: inline-block; }}
    .badge.pass {{ background: #E8F5E9; color: #2E7D32; }}
    .badge.fail {{ background: #FFEBEE; color: #C62828; }}
    .report-link {{ color: #C88A83; font-weight: 600; text-decoration: none; }}
    .report-link:hover {{ text-decoration: underline; }}
    .footer {{ margin-top: 2.5rem; font-size: 0.85rem; color: #8C847C; text-align: center; border-top: 1px solid #EBE5DF; padding-top: 1.5rem; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>AURA <span class="brand">LUXE</span> - Master Automation Test Execution Report</h1>
      <div class="meta">Automated Verification Across All 7 Testing Disciplines &bull; Executed on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-val">{len(results)}</div>
        <div class="stat-label">Total Test Suites</div>
      </div>
      <div class="stat-card">
        <div class="stat-val pass">{passed_count}</div>
        <div class="stat-label">Suites Passed</div>
      </div>
      <div class="stat-card">
        <div class="stat-val {'fail' if failed_count > 0 else ''}">{failed_count}</div>
        <div class="stat-label">Suites Failed</div>
      </div>
      <div class="stat-card">
        <div class="stat-val pass">{pass_rate}%</div>
        <div class="stat-label">Overall Pass Rate</div>
      </div>
    </div>

    <h2>Test Disciplines Summary Table</h2>
    <table>
      <thead>
        <tr>
          <th>Testing Discipline & Scope</th>
          <th>Duration</th>
          <th>Execution Result</th>
          <th>Detailed Report</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>

    <div class="footer">
      Generated automatically by Aura Luxe Automation Testing Framework. All assertions verified live.
    </div>
  </div>
</body>
</html>"""

    with open(MASTER_REPORT, "w", encoding="utf-8") as f:
        f.write(html)


def run_all():
    print("\n" + "=" * 70)
    print(" [*] AURA LUXE STORE - COMPLETE 7-DISCIPLINE TEST SUITE ORCHESTRATOR")
    print("=" * 70)
    print(f" Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Target Store: http://127.0.0.1:8000")
    print("=" * 70 + "\n")

    overall_start = time.time()
    results = []

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    for idx, suite in enumerate(TEST_SUITES, start=1):
        print(f"\n[{idx}/7] Running {suite['title']}...")
        print(f"      Scope: {suite['description']}")
        print("-" * 70)

        suite_start = time.time()
        res = subprocess.run([sys.executable, suite["runner"]], cwd=PROJECT_ROOT, env=env)
        duration = time.time() - suite_start
        passed = (res.returncode == 0)

        results.append({
            "id": suite["id"],
            "title": suite["title"],
            "description": suite["description"],
            "report": suite["report"],
            "duration": duration,
            "passed": passed
        })

    total_duration = time.time() - overall_start
    generate_master_html_report(results, total_duration)

    print("\n" + "=" * 70)
    print(" [*] ALL 7 AUTOMATION TEST SUITES FINISHED")
    print("=" * 70)
    print(f"{'DISCIPLINE':<28} | {'DURATION':<10} | {'STATUS'}")
    print("-" * 70)
    for r in results:
        status_str = "[PASS]" if r["passed"] else "[FAIL]"
        print(f"{r['title']:<28} | {r['duration']:>8.2f}s | {status_str}")
    print("=" * 70)
    print(f" Total Execution Time: {total_duration:.2f} seconds")
    print(f" [*] Master Executive Report: {MASTER_REPORT}")
    print(f" [*] Reports Directory: {REPORT_DIR}")
    print("=" * 70 + "\n")

    all_passed = all(r["passed"] for r in results)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_all())
