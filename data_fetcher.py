import requests

def fetch_nifty_data():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)
    data = response.json()
    return data