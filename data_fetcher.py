from nsepython import nse_optionchain_scrapper

def fetch_nifty_data():
    print("⏳ Fetching NIFTY option chain data...")
    try:
        data = nse_optionchain_scrapper("NIFTY")
        print("✅ Data fetch complete. Items:", len(data))
        return data
    except Exception as e:
        print("❌ Error fetching data from NSE:", e)
        return []
