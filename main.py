import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd

def run():
    st.title("📊 Zerodha NSE Instrument Fetcher")

    try:
        st.info("🔐 Initializing Zerodha API...")

        # Initialize KiteConnect using secrets
        kite = KiteConnect(api_key=st.secrets["zerodha"]["api_key"])
        kite.set_access_token(st.secrets["zerodha"]["access_token"])

        st.success("✅ Zerodha API initialized successfully!")

        st.info("📦 Fetching instrument list from Zerodha...")
        instruments = kite.instruments()

        if instruments:
            st.success(f"✅ Total instruments fetched: {len(instruments)}")
            df = pd.DataFrame(instruments)
            st.dataframe(df.head(20))  # Show first 20 rows
        else:
            st.warning("⚠️ No instruments found. Check your access token or try again later.")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    run()
