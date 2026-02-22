"""
============================================================
  browserstack_config.py
  BrowserStack driver factory & capabilities matrix
  PRODIGY INFOTECH — Task-04
============================================================
"""

import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

# ── BrowserStack Hub URL ─────────────────────────────────────
BS_USERNAME    = os.environ.get("BROWSERSTACK_USERNAME", "YOUR_USERNAME")
BS_ACCESS_KEY  = os.environ.get("BROWSERSTACK_ACCESS_KEY", "YOUR_ACCESS_KEY")
BS_HUB_URL     = f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

TARGET_URL     = "https://www.saucedemo.com"

# ── Shared BrowserStack Options ──────────────────────────────
COMMON_BS_OPTIONS = {
    "projectName"  : "Prodigy Infotech Task-04",
    "buildName"    : "Cross-Browser Login Suite v1.0",
    "networkLogs"  : True,
    "consoleLogs"  : "verbose",
    "video"        : True,
    "screenshots"  : True,
}

# ─────────────────────────────────────────────────────────────
#  BROWSER CAPABILITIES MATRIX
#  Each entry = one parallel session on BrowserStack
# ─────────────────────────────────────────────────────────────
BROWSER_MATRIX = [
    # ── Chrome / Windows 11 ──────────────────────────────────
    {
        "id"             : "chrome_win11",
        "label"          : "Chrome (Latest) · Windows 11",
        "browser"        : "chrome",
        "browser_version": "latest",
        "os"             : "Windows",
        "os_version"     : "11",
    },
    # ── Chrome / macOS Ventura ────────────────────────────────
    {
        "id"             : "chrome_ventura",
        "label"          : "Chrome (Latest) · macOS Ventura",
        "browser"        : "chrome",
        "browser_version": "latest",
        "os"             : "OS X",
        "os_version"     : "Ventura",
    },
    # ── Firefox / Windows 11 ─────────────────────────────────
    {
        "id"             : "firefox_win11",
        "label"          : "Firefox (Latest) · Windows 11",
        "browser"        : "firefox",
        "browser_version": "latest",
        "os"             : "Windows",
        "os_version"     : "11",
    },
    # ── Firefox / macOS Ventura ───────────────────────────────
    {
        "id"             : "firefox_ventura",
        "label"          : "Firefox (Latest) · macOS Ventura",
        "browser"        : "firefox",
        "browser_version": "latest",
        "os"             : "OS X",
        "os_version"     : "Ventura",
    },
    # ── Edge / Windows 11 ────────────────────────────────────
    {
        "id"             : "edge_win11",
        "label"          : "Edge (Latest) · Windows 11",
        "browser"        : "edge",
        "browser_version": "latest",
        "os"             : "Windows",
        "os_version"     : "11",
    },
    # ── Edge / Windows 10 ────────────────────────────────────
    {
        "id"             : "edge_win10",
        "label"          : "Edge (Latest-1) · Windows 10",
        "browser"        : "edge",
        "browser_version": "latest-1",
        "os"             : "Windows",
        "os_version"     : "10",
    },
    # ── Safari / macOS Sonoma ─────────────────────────────────
    {
        "id"             : "safari_sonoma",
        "label"          : "Safari 17 · macOS Sonoma",
        "browser"        : "safari",
        "browser_version": "17.0",
        "os"             : "OS X",
        "os_version"     : "Sonoma",
    },
    # ── Safari / macOS Ventura ────────────────────────────────
    {
        "id"             : "safari_ventura",
        "label"          : "Safari 16 · macOS Ventura",
        "browser"        : "safari",
        "browser_version": "16.0",
        "os"             : "OS X",
        "os_version"     : "Ventura",
    },
    # ── Mobile: iPhone 15 (Real Device) ──────────────────────
    {
        "id"          : "iphone15",
        "label"       : "Safari · iPhone 15 · iOS 17",
        "device"      : "iPhone 15",
        "os_version"  : "17",
        "browser"     : "safari",
        "real_mobile" : True,
    },
    # ── Mobile: Samsung Galaxy S23 (Real Device) ─────────────
    {
        "id"          : "galaxy_s23",
        "label"       : "Chrome · Galaxy S23 · Android 13",
        "device"      : "Samsung Galaxy S23",
        "os_version"  : "13.0",
        "browser"     : "chrome",
        "real_mobile" : True,
    },
    # ── Mobile: iPad 9th Gen ─────────────────────────────────
    {
        "id"          : "ipad_9th",
        "label"       : "Safari · iPad 9th Gen · iPadOS 15",
        "device"      : "iPad 9th",
        "os_version"  : "15",
        "browser"     : "safari",
        "real_mobile" : True,
    },
]


def build_capabilities(config: dict) -> dict:
    """Build W3C-compatible BrowserStack capabilities from a config dict."""
    bstack_options = {**COMMON_BS_OPTIONS}
    bstack_options["sessionName"] = config["label"]

    caps = {"bstack:options": bstack_options}

    if config.get("real_mobile"):
        # Mobile device caps
        bstack_options["deviceName"]  = config["device"]
        bstack_options["osVersion"]   = config["os_version"]
        bstack_options["realMobile"]  = "true"
        caps["browserName"] = config["browser"]
    else:
        # Desktop browser caps
        bstack_options["os"]             = config["os"]
        bstack_options["osVersion"]      = config["os_version"]
        bstack_options["browserVersion"] = config["browser_version"]
        caps["browserName"] = config["browser"]

    return caps


def create_driver(config: dict) -> WebDriver:
    """
    Instantiate a RemoteWebDriver connected to the BrowserStack Selenium Grid.
    """
    caps = build_capabilities(config)
    options_map = {
        "chrome"  : webdriver.ChromeOptions,
        "firefox" : webdriver.FirefoxOptions,
        "edge"    : webdriver.EdgeOptions,
        "safari"  : webdriver.SafariOptions,
    }

    browser_name = config.get("browser", "chrome").lower()
    OptionsClass = options_map.get(browser_name, webdriver.ChromeOptions)
    options = OptionsClass()

    for key, val in caps.items():
        options.set_capability(key, val)

    driver = webdriver.Remote(
        command_executor=BS_HUB_URL,
        options=options,
    )
    driver.implicitly_wait(10)
    return driver
