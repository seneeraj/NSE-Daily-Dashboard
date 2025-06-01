import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import matplotlib.pyplot as plt

# Fetch instruments from Zerodha
@st.cache_data(show_spinner="Fetching instruments from Zerodha...")
def get_instruments(api_key, access_token):
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    instruments = kite.instruments()
    return pd.DataFrame(instruments)

# Fetch real-time Open Interest for NIFTY options
def fetch_oi_data(kite, df):
    tokens = df['instrument_token'].tolist()
    quotes = kite.quote(tokens)
    df['open_interest'] = df['instrument_token'].apply(lambda x: quotes.get(str(x), {}).get("oi", 0))
    return df

# Plot OI buildup
def plot_oi_chart(df):
    oi_df = df[['strike', 'instrument_type', 'open_interest']].copy()
    grouped = oi_df.groupby(['strike', 'instrument_type'])['open_interest'].sum().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(12, 5))
    grouped['CE'].plot(kind='bar', color='skyblue', width=0.4, position=1, label='Call OI', ax=ax)
    grouped['PE'].plot(kind='bar', color='orange', width=0.4, position=0, label='Put OI', ax=ax)
    ax.set_title("NIFTY Option Chain OI Buildup")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Open Interest")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Main Streamlit app
def main():
    st.set_page_config(page_title="Zerodha Option Chain with OI Chart", layout="wide")
    st.title("📊 NIFTY Option Chain Viewer with OI Buildup Chart")

    try:
        api_key = st.secrets["zerodha"]["api_key"]
        access_token = st.secrets["zerodha"]["access_token"]
    except KeyError:
        st.error("❌ Missing Zerodha credentials in Streamlit secrets.")
        return

    try:
        df_all = get_instruments(api_key, access_token)
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)

        df_nifty = df_all[(df_all['name'] == 'NIFTY') & (df_all['segment'] == 'NFO-OPT')]

        # Show top 20 option contracts
        st.subheader("📈 NIFTY Option Chain (Top 20)")
        st.dataframe(df_nifty.head(20))

        st.subheader("📊 OI Buildup Chart")
        df_nifty = fetch_oi_data(kite, df_nifty)
        plot_oi_chart(df_nifty)

    except Exception as e:
        st.error(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
