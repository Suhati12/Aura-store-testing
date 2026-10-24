"""
Pytest configuration and global fixtures for Aura Luxe Store testing suite.
Provides automated server startup, base URL management, and Playwright browser fixtures.
"""

import os
import sys
import time
import threading
import pytest
import requests
from werkzeug.serving import make_server

# Add workspace root to sys.path so server can be imported
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

import server

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


@pytest.fixture(scope="session", autouse=True)
def live_server():
    """
    Ensure the Aura Luxe Flask backend & web server is running.
    If not already running on port 8000, starts it in a background daemon thread.
    """
    already_running = False
    try:
        res = requests.get(f"{BASE_URL}/api/health", timeout=1.0)
        if res.status_code == 200:
            already_running = True
    except Exception:
        already_running = False

    srv = None
    if not already_running:
        srv = make_server(SERVER_HOST, SERVER_PORT, server.app, threaded=True)
        t = threading.Thread(target=srv.serve_forever, daemon=True)
        t.start()

        # Wait for server to come alive
        for _ in range(30):
            try:
                res = requests.get(f"{BASE_URL}/api/health", timeout=0.5)
                if res.status_code == 200:
                    break
            except Exception:
                time.sleep(0.1)

    yield BASE_URL

    if srv is not None:
        srv.shutdown()


@pytest.fixture(scope="session")
def base_url():
    """Return the base URL of the running test application."""
    return BASE_URL


@pytest.fixture(scope="session")
def screenshots_dir():
    """Return the directory path for saving test screenshots and ensure it exists."""
    reports_dir = os.path.join(WORKSPACE_ROOT, "reports", "screenshots")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir
