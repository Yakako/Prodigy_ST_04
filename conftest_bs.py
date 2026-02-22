"""
conftest.py
Pytest shared hooks and fixtures for BrowserStack cross-browser test suite.
PRODIGY INFOTECH — Task-04
"""

import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "positive: Happy-path login tests")
    config.addinivalue_line("markers", "negative: Failure-path login tests")
    config.addinivalue_line("markers", "ui: UI/layout/responsiveness tests")
    config.addinivalue_line("markers", "security: Security validation tests")
    config.addinivalue_line("markers", "form: Form submission behaviour tests")


def pytest_html_report_title(report):
    report.title = "Prodigy Infotech — Task-04 Cross-Browser Test Report"


def pytest_html_env(report, environment):
    environment["Project"]      = "Task-04 BrowserStack Cross-Browser Testing"
    environment["Organization"] = "Prodigy Infotech"
    environment["Target"]       = "https://www.saucedemo.com"
    environment["Grid"]         = "BrowserStack Selenium Grid"
    environment["Browsers"]     = "Chrome, Firefox, Safari, Edge"
    environment["Devices"]      = "Desktop + Mobile (Real Device Cloud)"
    environment["Parallelism"]  = "11 sessions in parallel"


# ── Capture pass/fail for BrowserStack session tagging ────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
