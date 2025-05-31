import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd

# Caching the fetch operation
@st.cache_data(show_spinner="Fetching instruments from Zerodha...")
def get_instruments(api_key, access_token):
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    instruments = kite.instruments()
    return pd.DataFrame(instruments)

def main():
    st.set_page_config(page_title="Zerodha Option Chain Dashboard", layout="wide")
    st.title("📊 Zerodha NSE Option Chain Viewer")

    # Load secrets
    try:
        api_key = st.secrets["zerodha"]["api_key"]
        access_token = st.secrets["zerodha"]["access_token"]
    except KeyError:
        st.error("❌ API Key or Access Token missing in secrets. Please configure them.")
        return

    try:
        df = get_instruments(api_key, access_token)
        st.success(f"✅ Instruments fetched: {len(df)}")
        st.dataframe(df.head(20))

        # Optional: Filter for NIFTY options
        nifty_opt = df[(df['name'] == 'NIFTY') & (df['segment'] == 'NFO-OPT')]
        st.subheader("📈 NIFTY Option Chain (Top 20)")
        st.dataframe(nifty_opt.head(20))

    except Exception as e:
        st.error(f"❌ Failed to fetch instruments: {e}")

if __name__ == "__main__":
    main()
