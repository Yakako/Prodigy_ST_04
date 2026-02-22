# 🌐 Cross-Browser Testing with BrowserStack
### Prodigy Infotech — Task-04

> Automated cross-browser and cross-device login/form testing powered by **BrowserStack Selenium Grid**, using **Pytest** + **Selenium WebDriver**.

---

## 📁 Project Structure

```
browserstack_suite/
│
├── tests/
│   └── test_crossbrowser_login.py   # All cross-browser test cases
│
├── reports/                         # Auto-generated HTML test reports
│
├── browserstack.yml                 # BrowserStack SDK config (browser matrix)
├── browserstack_config.py           # Driver factory & capabilities builder
├── conftest.py                      # Pytest hooks, fixtures, report metadata
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## ⚙️ Setup

### 1. Prerequisites
- Python 3.8+
- A **BrowserStack account** with Automate access
- Your BrowserStack **Username** and **Access Key** from the Automate dashboard

### 2. Install Dependencies
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set BrowserStack Credentials
```bash
# Linux / macOS
export BROWSERSTACK_USERNAME="your_username"
export BROWSERSTACK_ACCESS_KEY="your_access_key"

# Windows PowerShell
$env:BROWSERSTACK_USERNAME="your_username"
$env:BROWSERSTACK_ACCESS_KEY="your_access_key"
```

---

## ▶️ Running the Tests

### Run All Tests (11 browsers in parallel)
```bash
pytest
```

### Run via BrowserStack SDK (recommended)
```bash
browserstack-sdk pytest tests/test_crossbrowser_login.py
```

### Run Only Positive Tests
```bash
pytest -k "Positive"
```

### Run Only on Specific Browser
```bash
pytest -k "chrome_win11"
```

### Run Only Negative Tests
```bash
pytest -k "Negative"
```

### Generate Report
```bash
pytest --html=reports/crossbrowser_report.html --self-contained-html
```

---

## 🌐 Browser & Device Matrix (11 Configurations)

### Desktop Browsers
| ID | Browser | Version | OS |
|---|---|---|---|
| `chrome_win11` | Chrome | Latest | Windows 11 |
| `chrome_ventura` | Chrome | Latest | macOS Ventura |
| `firefox_win11` | Firefox | Latest | Windows 11 |
| `firefox_ventura` | Firefox | Latest | macOS Ventura |
| `edge_win11` | Edge | Latest | Windows 11 |
| `edge_win10` | Edge | Latest-1 | Windows 10 |
| `safari_sonoma` | Safari | 17.0 | macOS Sonoma |
| `safari_ventura` | Safari | 16.0 | macOS Ventura |

### Real Mobile Devices
| ID | Device | OS | Browser |
|---|---|---|---|
| `iphone15` | iPhone 15 | iOS 17 | Safari |
| `galaxy_s23` | Samsung Galaxy S23 | Android 13 | Chrome |
| `ipad_9th` | iPad 9th Gen | iPadOS 15 | Safari |

---

## 🧪 Test Case Summary (24 total × 11 browsers = 264 sessions)

### ✅ Positive Cases (6)
| ID | Test |
|---|---|
| POS-01 | Valid login → dashboard redirect |
| POS-02 | Inventory list visible after login |
| POS-03 | Page title correct post-login |
| POS-04 | Enter key submits form |
| POS-05 | No error on valid login |
| POS-06 | Logout returns to login page |

### ❌ Negative Cases (10)
| ID | Test |
|---|---|
| NEG-01 | Wrong password → error shown |
| NEG-02 | Wrong username → error shown |
| NEG-03 | Empty username → required error |
| NEG-04 | Empty password → required error |
| NEG-05 | Both fields empty → blocked |
| NEG-06 | Locked user → locked-out message |
| NEG-07 | SQL injection → denied |
| NEG-08 | XSS payload → rejected |
| NEG-09 | Wrong-case password → rejected |
| NEG-10 | Whitespace username → rejected |

### 🎨 UI / Layout Cases (8)
| ID | Test |
|---|---|
| UI-01 | All form elements present |
| UI-02 | Password field is masked |
| UI-03 | Login button label correct |
| UI-04 | Error message styled & visible |
| UI-05 | Page logo renders |
| UI-06 | Field placeholders present |
| UI-07 | No horizontal scroll |
| UI-08 | Tab key navigation works |

---

## 🔍 Viewing Results on BrowserStack

After running tests, visit your **BrowserStack Automate dashboard** at:
`https://automate.browserstack.com/dashboard`

Each test session will show:
- ✅ / ❌ Pass/Fail status
- 📹 Video recording of the session
- 📸 Screenshots at each step
- 🌐 Network activity logs
- 🖥️ Console logs

---

## 🛠️ Technology Stack

| Tool | Purpose |
|---|---|
| **Pytest** | Test runner and assertion library |
| **Selenium 4 (W3C)** | Browser automation protocol |
| **BrowserStack Automate** | Cloud browser & device grid (3,000+ combinations) |
| **pytest-xdist** | Parallel session execution |
| **pytest-html** | Local HTML report generation |
| **BrowserStack SDK** | Auto capability injection & result sync |

---

*Prodigy Infotech — QA Automation Division | Task-04 | Feb 2026*
