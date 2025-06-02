import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import matplotlib.pyplot as plt

# Set page config as the first Streamlit command
st.set_page_config(page_title="Zerodha Option Chain with OI Chart", layout="wide")

# Debugging: Check if secrets are loaded
st.write("✅ Secrets loaded:", st.secrets["zerodha"]["api_key"])

# 1. Initialize KiteConnect (global)
def get_kite():
    api_key = st.secrets["zerodha"]["api_key"]
    access_token = st.secrets["zerodha"]["access_token"]
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite

# 2. Fetch instruments and cache them (fix: ignore hashing of KiteConnect object)
@st.cache_data(show_spinner="Fetching instruments from Zerodha...")
def get_instruments(_kite):
    instruments = _kite.instruments()
    return pd.DataFrame(instruments)

# 3. Fetch OI using live quote API
def fetch_oi_data(kite, df):
    tokens = df['instrument_token'].tolist()
    quotes = kite.quote(tokens)
    df['open_interest'] = df['instrument_token'].apply(lambda x: quotes.get(str(x), {}).get("oi", 0))
    return df

# 4. Plot OI Chart
def plot_oi_chart(df):
    oi_df = df[['strike', 'instrument_type', 'open_interest']].copy()
    grouped = oi_df.groupby(['strike', 'instrument_type'])['open_interest'].sum().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(12, 5))
    if 'CE' in grouped.columns:
        grouped['CE'].plot(kind='bar', color='skyblue', width=0.4, position=1, label='Call OI', ax=ax)
    if 'PE' in grouped.columns:
        grouped['PE'].plot(kind='bar', color='orange', width=0.4, position=0, label='Put OI', ax=ax)

    ax.set_title("NIFTY Option Chain OI Buildup")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Open Interest")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 5. Main App
def main():
    st.title("📊 NIFTY Option Chain Viewer with OI Buildup Chart")

    try:
        kite = get_kite()
        df_all = get_instruments(kite)

        # Filter NIFTY options
        df_nifty = df_all[(df_all['name'] == 'NIFTY') & (df_all['segment'] == 'NFO-OPT')]

        st.subheader("📈 NIFTY Option Chain (Top 20)")
        st.dataframe(df_nifty.head(20))

        st.subheader("📊 OI Buildup Chart")
        df_nifty = fetch_oi_data(kite, df_nifty)
        plot_oi_chart(df_nifty)

    except Exception as e:
        st.error(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
