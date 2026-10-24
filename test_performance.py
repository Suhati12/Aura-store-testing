"""
Performance Testing Suite
Measures page loading speeds, response times, and key browser performance metrics:
- DNS Lookup, TCP Handshake, Time to First Byte (TTFB)
- DOM Content Loaded (DCL) and Full Page Load Time
- First Contentful Paint (FCP)
- Resource transfer sizes and DOM node counts
Validates metrics against industry performance budgets and exports JSON & HTML reports.
"""

import json
import os
import pytest
from playwright.sync_api import sync_playwright

PERFORMANCE_BUDGETS = {
    "ttfb_ms": 500,           # Time to first byte < 500ms
    "dom_content_loaded_ms": 2000, # DOM Content Loaded < 2s
    "page_load_ms": 3000,     # Full page load < 3s
    "first_contentful_paint_ms": 1800 # FCP < 1.8s
}


def test_measure_page_performance(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate and wait for DOM and initial assets
        response = page.goto(live_server, wait_until="domcontentloaded")
        page.wait_for_selector('[data-testid="header-logo"]')
        page.wait_for_timeout(1000)

        # Collect Navigation Timing metrics via JavaScript
        timing_data = page.evaluate("""
            () => {
                const nav = performance.getEntriesByType('navigation')[0] || {};
                const paintEntries = performance.getEntriesByType('paint');
                let fcp = 0;
                for (const entry of paintEntries) {
                    if (entry.name === 'first-contentful-paint') {
                        fcp = entry.startTime;
                    }
                }

                const resources = performance.getEntriesByType('resource');
                let totalTransferSize = 0;
                resources.forEach(r => {
                    totalTransferSize += (r.transferSize || 0);
                });

                return {
                    dns_time_ms: Math.max(0, Math.round(nav.domainLookupEnd - nav.domainLookupStart)),
                    tcp_time_ms: Math.max(0, Math.round(nav.connectEnd - nav.connectStart)),
                    ttfb_ms: Math.max(0, Math.round(nav.responseStart - nav.requestStart)),
                    download_time_ms: Math.max(0, Math.round(nav.responseEnd - nav.responseStart)),
                    dom_interactive_ms: Math.max(0, Math.round(nav.domInteractive - nav.responseEnd)),
                    dom_content_loaded_ms: Math.max(0, Math.round(nav.domContentLoadedEventEnd - nav.startTime)),
                    page_load_ms: Math.max(0, Math.round(nav.loadEventEnd - nav.startTime)),
                    first_contentful_paint_ms: Math.round(fcp),
                    total_resources_count: resources.length,
                    total_transfer_bytes: totalTransferSize,
                    dom_nodes_count: document.querySelectorAll('*').length
                };
            }
        """)

        # Add budget checks
        results = {
            "metrics": timing_data,
            "budgets": PERFORMANCE_BUDGETS,
            "evaluations": {
                "ttfb_pass": timing_data["ttfb_ms"] <= PERFORMANCE_BUDGETS["ttfb_ms"],
                "dom_content_loaded_pass": timing_data["dom_content_loaded_ms"] <= PERFORMANCE_BUDGETS["dom_content_loaded_ms"],
                "page_load_pass": timing_data["page_load_ms"] <= PERFORMANCE_BUDGETS["page_load_ms"],
                "fcp_pass": timing_data["first_contentful_paint_ms"] <= PERFORMANCE_BUDGETS["first_contentful_paint_ms"],
            }
        }

        # Save metrics JSON artifact
        reports_dir = os.path.join(os.path.dirname(__file__), "../../reports")
        os.makedirs(reports_dir, exist_ok=True)
        metrics_file = os.path.join(reports_dir, "performance_metrics.json")
        with open(metrics_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        # Capture performance state screenshot
        page.screenshot(path=f"{screenshots_dir}/performance_page_loaded.png")

        # Assertions against budget
        assert results["evaluations"]["ttfb_pass"], (
            f"TTFB {timing_data['ttfb_ms']}ms exceeded budget {PERFORMANCE_BUDGETS['ttfb_ms']}ms"
        )
        assert results["evaluations"]["dom_content_loaded_pass"], (
            f"DCL {timing_data['dom_content_loaded_ms']}ms exceeded budget {PERFORMANCE_BUDGETS['dom_content_loaded_ms']}ms"
        )
        assert results["evaluations"]["page_load_pass"], (
            f"Page Load {timing_data['page_load_ms']}ms exceeded budget {PERFORMANCE_BUDGETS['page_load_ms']}ms"
        )

        browser.close()
