"""
============================================================
  tests/test_crossbrowser_login.py
  Cross-Browser Login & Form Submission Tests
  PRODIGY INFOTECH — Task-04 | BrowserStack Selenium Grid
  Target: https://www.saucedemo.com
============================================================

Test Categories:
  [POS] Positive — successful login flows
  [NEG] Negative — invalid credential / empty field flows
  [UI]  UI/UX    — layout, element visibility, responsiveness
  [FORM] Form    — submission behaviour, field validation
============================================================
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from browserstack_config import create_driver, BROWSER_MATRIX, TARGET_URL

# ─────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────
VALID_USER     = "standard_user"
VALID_PASS     = "secret_sauce"
LOCKED_USER    = "locked_out_user"
PROBLEM_USER   = "problem_user"
PERF_USER      = "performance_glitch_user"
DASHBOARD_PATH = "/inventory.html"
TIMEOUT        = 15   # seconds

# ─────────────────────────────────────────────────────────────
#  PYTEST PARAMETRIZE — run every test on every browser config
# ─────────────────────────────────────────────────────────────
@pytest.fixture(params=BROWSER_MATRIX, ids=lambda c: c["id"])
def browser(request):
    """
    Fixture: spins up one BrowserStack remote session per config entry.
    Marks the BrowserStack session pass/fail on teardown.
    """
    config = request.param
    driver = create_driver(config)
    driver.get(TARGET_URL)
    yield driver, config

    # ── Report result back to BrowserStack dashboard ──────────
    test_passed = not hasattr(request.node, "rep_call") or request.node.rep_call.passed
    status  = "passed" if test_passed else "failed"
    reason  = "Test passed" if test_passed else str(getattr(request.node, "rep_call", ""))
    driver.execute_script(
        f'browserstack_executor: {{"action":"setSessionStatus","arguments":{{"status":"{status}","reason":"{reason}"}}}}'
    )
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ─────────────────────────────────────────────────────────────
#  SHARED HELPERS
# ─────────────────────────────────────────────────────────────
def fill_login(driver, username: str, password: str):
    """Clear and populate both login fields."""
    u = driver.find_element(By.ID, "user-name")
    p = driver.find_element(By.ID, "password")
    u.clear(); u.send_keys(username)
    p.clear(); p.send_keys(password)


def submit_login(driver):
    driver.find_element(By.ID, "login-button").click()


def get_error(driver) -> str:
    try:
        el = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        return el.text.strip()
    except NoSuchElementException:
        return ""


def on_dashboard(driver) -> bool:
    return DASHBOARD_PATH in driver.current_url


def wait_for_dashboard(driver, timeout=TIMEOUT) -> bool:
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains("inventory"))
        return True
    except TimeoutException:
        return False


def element_visible(driver, by, locator) -> bool:
    try:
        return driver.find_element(by, locator).is_displayed()
    except NoSuchElementException:
        return False


# ─────────────────────────────────────────────────────────────
#  POSITIVE TEST CASES
# ─────────────────────────────────────────────────────────────

class TestPositiveCrossBrowser:

    def test_valid_login_redirects_to_dashboard(self, browser):
        """
        [POS-01] Valid credentials → user is redirected to /inventory.html.
        Runs on every browser/device in the matrix.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, VALID_PASS)
        submit_login(driver)
        assert wait_for_dashboard(driver), (
            f"[{cfg['label']}] Expected redirect to dashboard. URL: {driver.current_url}"
        )

    def test_inventory_list_visible_after_login(self, browser):
        """
        [POS-02] After login the products grid should be visible.
        Validates that the DOM renders the inventory correctly across all browsers.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, VALID_PASS)
        submit_login(driver)
        wait_for_dashboard(driver)
        assert element_visible(driver, By.CLASS_NAME, "inventory_list"), (
            f"[{cfg['label']}] Inventory list not displayed after login."
        )

    def test_page_title_post_login(self, browser):
        """
        [POS-03] Browser tab title should read 'Swag Labs' after login.
        Catches browsers that might strip or mangle the <title> tag.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, VALID_PASS)
        submit_login(driver)
        wait_for_dashboard(driver)
        assert "Swag Labs" in driver.title, (
            f"[{cfg['label']}] Unexpected title: '{driver.title}'"
        )

    def test_enter_key_submits_login_form(self, browser):
        """
        [POS-04] Pressing Enter in the password field submits the form.
        Some browsers differ in how they dispatch keyboard events.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, VALID_PASS)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        assert wait_for_dashboard(driver), (
            f"[{cfg['label']}] Enter key did not submit the login form."
        )

    def test_no_error_on_valid_login(self, browser):
        """
        [POS-05] No error element should appear on a successful login.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, VALID_PASS)
        submit_login(driver)
        wait_for_dashboard(driver)
        err = get_error(driver)
        assert err == "", f"[{cfg['label']}] Unexpected error: '{err}'"

    def test_logout_and_return_to_login(self, browser):
        """
        [POS-06] User can log in, open the menu, log out, and is returned
        to the login page. Validates navigation across all browsers.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, VALID_PASS)
        submit_login(driver)
        wait_for_dashboard(driver)

        # Open hamburger menu → click Logout
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(0.8)   # menu animation
        WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        ).click()

        WebDriverWait(driver, TIMEOUT).until(EC.url_to_be(TARGET_URL + "/"))
        assert driver.current_url.rstrip("/") == TARGET_URL, (
            f"[{cfg['label']}] Logout did not return to login page."
        )


# ─────────────────────────────────────────────────────────────
#  NEGATIVE TEST CASES
# ─────────────────────────────────────────────────────────────

class TestNegativeCrossBrowser:

    def test_wrong_password_blocked(self, browser):
        """
        [NEG-01] Valid username + wrong password → error message shown,
        user stays on login page.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, "bad_password!")
        submit_login(driver)
        err = get_error(driver)
        assert "do not match" in err.lower(), (
            f"[{cfg['label']}] Expected mismatch error. Got: '{err}'"
        )
        assert not on_dashboard(driver)

    def test_wrong_username_blocked(self, browser):
        """
        [NEG-02] Non-existent username + valid password → error shown.
        """
        driver, cfg = browser
        fill_login(driver, "ghost_user_9999", VALID_PASS)
        submit_login(driver)
        err = get_error(driver)
        assert err != "", f"[{cfg['label']}] No error shown for unknown username."
        assert not on_dashboard(driver)

    def test_empty_username_required(self, browser):
        """
        [NEG-03] Empty username field → 'Username is required' error.
        Validates that browser doesn't skip form validation.
        """
        driver, cfg = browser
        fill_login(driver, "", VALID_PASS)
        submit_login(driver)
        err = get_error(driver)
        assert "Username is required" in err, (
            f"[{cfg['label']}] Expected username-required error. Got: '{err}'"
        )

    def test_empty_password_required(self, browser):
        """
        [NEG-04] Valid username, empty password → 'Password is required' error.
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, "")
        submit_login(driver)
        err = get_error(driver)
        assert "Password is required" in err, (
            f"[{cfg['label']}] Expected password-required error. Got: '{err}'"
        )

    def test_both_fields_empty(self, browser):
        """
        [NEG-05] Both fields empty → form refuses to submit.
        """
        driver, cfg = browser
        submit_login(driver)   # click without filling anything
        err = get_error(driver)
        assert err != "", f"[{cfg['label']}] No error shown when both fields empty."
        assert not on_dashboard(driver)

    def test_locked_user_denied(self, browser):
        """
        [NEG-06] Locked-out user account → descriptive locked-out message.
        """
        driver, cfg = browser
        fill_login(driver, LOCKED_USER, VALID_PASS)
        submit_login(driver)
        err = get_error(driver)
        assert "locked out" in err.lower(), (
            f"[{cfg['label']}] Expected locked-out message. Got: '{err}'"
        )
        assert not on_dashboard(driver)

    def test_sql_injection_rejected(self, browser):
        """
        [NEG-07] SQL injection payloads in both fields → access denied.
        Validates consistent security posture across all browsers.
        """
        driver, cfg = browser
        fill_login(driver, "' OR 1=1 --", "' OR '1'='1")
        submit_login(driver)
        assert not on_dashboard(driver), (
            f"[{cfg['label']}] SQL injection should not grant dashboard access!"
        )

    def test_xss_payload_rejected(self, browser):
        """
        [NEG-08] XSS payload in username → not executed, access denied.
        """
        driver, cfg = browser
        fill_login(driver, "<script>alert('xss')</script>", VALID_PASS)
        submit_login(driver)
        assert not on_dashboard(driver), (
            f"[{cfg['label']}] XSS payload bypassed login!"
        )

    def test_case_sensitive_password(self, browser):
        """
        [NEG-09] Uppercased password variant is rejected (case-sensitivity check).
        """
        driver, cfg = browser
        fill_login(driver, VALID_USER, "SECRET_SAUCE")
        submit_login(driver)
        assert not on_dashboard(driver), (
            f"[{cfg['label']}] Case-insensitive password accepted — security issue!"
        )

    def test_whitespace_username_rejected(self, browser):
        """
        [NEG-10] Username consisting only of spaces → rejected.
        """
        driver, cfg = browser
        fill_login(driver, "     ", VALID_PASS)
        submit_login(driver)
        assert not on_dashboard(driver), (
            f"[{cfg['label']}] Whitespace-only username should not authenticate."
        )


# ─────────────────────────────────────────────────────────────
#  UI / LAYOUT / RESPONSIVENESS TESTS
# ─────────────────────────────────────────────────────────────

class TestUICrossBrowser:

    def test_login_form_elements_present(self, browser):
        """
        [UI-01] All critical form elements must be visible on page load.
        Catches browsers that fail to render key DOM elements.
        """
        driver, cfg = browser
        assert element_visible(driver, By.ID, "user-name"),    f"[{cfg['label']}] Username field missing."
        assert element_visible(driver, By.ID, "password"),     f"[{cfg['label']}] Password field missing."
        assert element_visible(driver, By.ID, "login-button"), f"[{cfg['label']}] Login button missing."

    def test_password_field_type(self, browser):
        """
        [UI-02] Password field must have type='password' (masked input).
        Safari on iOS has historically shown plain text for type mismatches.
        """
        driver, cfg = browser
        field = driver.find_element(By.ID, "password")
        assert field.get_attribute("type") == "password", (
            f"[{cfg['label']}] Password field type is '{field.get_attribute('type')}', expected 'password'."
        )

    def test_login_button_label(self, browser):
        """
        [UI-03] Login button value should be 'Login'.
        """
        driver, cfg = browser
        btn = driver.find_element(By.ID, "login-button")
        label = (btn.get_attribute("value") or btn.text).strip().lower()
        assert "login" in label, (
            f"[{cfg['label']}] Button label unexpected: '{label}'"
        )

    def test_error_message_styling_visible(self, browser):
        """
        [UI-04] After a failed login, the error message container must be
        visible and styled. Catches CSS rendering issues across browsers.
        """
        driver, cfg = browser
        fill_login(driver, "", "")
        submit_login(driver)
        try:
            err_el = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            assert err_el.is_displayed(), f"[{cfg['label']}] Error element hidden."
            assert err_el.value_of_css_property("color") != "", (
                f"[{cfg['label']}] Error element has no color style."
            )
        except NoSuchElementException:
            pytest.fail(f"[{cfg['label']}] Error element not found in DOM.")

    def test_page_logo_renders(self, browser):
        """
        [UI-05] The Swag Labs logo image/div on the login page must render.
        Validates asset loading across browsers.
        """
        driver, cfg = browser
        logo = element_visible(driver, By.CLASS_NAME, "login_logo")
        assert logo, f"[{cfg['label']}] Login logo not rendered."

    def test_form_field_placeholders(self, browser):
        """
        [UI-06] Username and password inputs must have non-empty placeholders.
        """
        driver, cfg = browser
        u_placeholder = driver.find_element(By.ID, "user-name").get_attribute("placeholder")
        p_placeholder = driver.find_element(By.ID, "password").get_attribute("placeholder")
        assert u_placeholder and len(u_placeholder) > 0, (
            f"[{cfg['label']}] Username placeholder empty."
        )
        assert p_placeholder and len(p_placeholder) > 0, (
            f"[{cfg['label']}] Password placeholder empty."
        )

    def test_viewport_no_horizontal_scroll(self, browser):
        """
        [UI-07] No horizontal scrollbar should appear on the login page.
        Critical for mobile browsers and narrow viewports.
        """
        driver, cfg = browser
        scroll_width  = driver.execute_script("return document.documentElement.scrollWidth")
        client_width  = driver.execute_script("return document.documentElement.clientWidth")
        assert scroll_width <= client_width, (
            f"[{cfg['label']}] Horizontal overflow detected: "
            f"scrollWidth={scroll_width}, clientWidth={client_width}"
        )

    def test_tab_key_navigation(self, browser):
        """
        [UI-08] Tab key should move focus from username → password → button.
        Accessibility compliance across browsers.
        """
        driver, cfg = browser
        username_field = driver.find_element(By.ID, "user-name")
        username_field.click()
        username_field.send_keys(Keys.TAB)
        focused_id = driver.execute_script("return document.activeElement.id")
        assert focused_id == "password", (
            f"[{cfg['label']}] Tab did not move focus to password field. Focused: '{focused_id}'"
        )
