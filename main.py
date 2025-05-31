import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from kiteconnect import KiteConnect

# CONFIGURATION
API_KEY = st.secrets["zerodha"]["api_key"]
API_SECRET = st.secrets["zerodha"]["api_secret"]
ACCESS_TOKEN = st.secrets["zerodha"]["access_token"]

# Initialize Kite Connect
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# Fetch instruments once
@st.cache_data
def get_instruments():
    return pd.DataFrame(kite.instruments("NSE"))

instruments = kite.instruments()
print(f"Total instruments: {len(instruments)}")
print(instruments[:5])  # Print first 5 entries for verification

# Get NIFTY option chain data
def get_option_chain(symbol="NIFTY"):
    all_instruments = get_instruments()
    oc = all_instruments[
        (all_instruments['name'] == symbol) &
        (all_instruments['segment'] == 'NFO-OPT') &
        (all_instruments['expiry'] == all_instruments['expiry'].min())  # nearest expiry
    ]
    return oc

# Main Dashboard
def main():
    st.title("📈 Zerodha NIFTY Option Chain Dashboard")

    df = get_option_chain()

    st.write("Fetched Instruments:", df.shape[0])

    # Prepare for OI visualization
    calls = df[df['instrument_type'] == 'CE']
    puts = df[df['instrument_type'] == 'PE']

    merged = pd.merge(
        calls[['strike', 'last_price', 'instrument_token']],
        puts[['strike', 'last_price', 'instrument_token']],
        on='strike',
        suffixes=('_call', '_put')
    )

    # Plot chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(merged['strike'], merged['last_price_call'], label='Call Price', color='green')
    ax.plot(merged['strike'], merged['last_price_put'], label='Put Price', color='red')
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Price")
    ax.set_title("Call vs Put Prices - NIFTY Option Chain")
    ax.legend()
    st.pyplot(fig)

if __name__ == "__main__":
    main()
