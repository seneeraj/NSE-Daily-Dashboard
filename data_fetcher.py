from nsepython import nse_optionchain_scrapper

def fetch_nifty_data():
    try:
        data = nse_optionchain_scrapper("NIFTY")
        return data
    except Exception as e:
        print("❌ Error fetching data from NSE:", e)
        return {}
