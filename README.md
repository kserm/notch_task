# Contact Form Automated Testing Suite

## Overview
This project provides automated testing for the Notch contact form (https://wearenotch.com/contact/) using Playwright with Python. The test suite follows industry best practices including the Page Object Model pattern and provides both mocked and real form submission testing capabilities.

## Prerequisites

- Python: 3.8 or higher
- pip: Python package installer
- Git: For cloning the repository (optional)

## Installation & Setup

### Clone or Download the Project
*Option 1: Clone with Git*
```bash
git clone <repository-url>
```

```bash
cd notch_task
```

*Option 2: Download and extract ZIP file*
Extract to desired directory and navigate to it

### Create Virtual Environment (Recommended)
Create virtual environment:
```bash
python -m venv .venv
```
or
```bash
# Linux
python3 -m venv .venv
```

**Activate virtual environment**
*On Windows:*
```
.venv\Scripts\activate
```
*On macOS/Linux:*
```bash
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Playwright Browsers
Install browser binaries (required for first-time setup)
```bash
playwright install
```

## Running Tests

### Test Execution

Run all tests in headless mode:
```bash
pytest tests/ --html=reports/report.html -v
```

Run specific test method:
```bash
pytest tests/test_contact_page.py::TestContactPage::test_page_loads_successfully --html=reports/report.html -v
```

Run in headful mode (see browser actions):
```bash
pytest tests/ --html=reports/report.html -v --headed --slowmo 500
```
*Note: adjust actions delay time with `--slowmo <time_in_ms>` options*

Run with specific browser:
```bash
# Firefox
pytest tests/ --html=reports/report.html -v --browser firefox
```
or
```bash
# Safari engine
pytest tests/ --html=reports/report.html -v --browser webkit
```

## Configuration Options
Edit helpers.py to modify test behavior:

`ROUTE_INTERCEPTION = False  # Set to True for mocked submissions`