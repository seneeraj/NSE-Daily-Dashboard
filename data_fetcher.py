from playwright.sync_api import sync_playwright
import json

def fetch_nifty_data():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com"
        })

        try:
            page.goto("https://www.nseindia.com", timeout=10000)
            page.wait_for_timeout(2000)  # 2 sec wait
            response = page.request.get(url)
            data = response.json()
            browser.close()
            return data
        except Exception as e:
            print(f"⚠️ Error fetching data with Playwright: {e}")
            browser.close()
            return {}
