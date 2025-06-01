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

        # Calculate Open Interest chart data (top 20 strikes with CE/PE)
        nifty_opt_oi = nifty_opt[nifty_opt["expiry"] == nifty_opt["expiry"].min()]  # Nearest expiry
        oi_data = nifty_opt_oi[["strike", "instrument_type", "instrument_token"]].copy()
        
        # Get live OI data
        from kiteconnect import KiteTicker  # only if you plan to use WebSocket, else stick with quote
        tokens = oi_data["instrument_token"].tolist()
        quotes = kite.quote(tokens)
        oi_data["open_interest"] = oi_data["instrument_token"].apply(lambda x: quotes[str(x)]["oi"])
        
        # Pivot data to Strike vs [CE, PE]
        pivot = oi_data.pivot_table(index="strike", columns="instrument_type", values="open_interest", fill_value=0)
        pivot = pivot.sort_index().tail(20)  # show last 20 strike prices
        
        # Plot the chart
        st.subheader("📊 OI Buildup Chart (CE vs PE)")
        fig, ax = plt.subplots(figsize=(10, 5))
        pivot["CE"].plot(kind="bar", color="skyblue", width=0.4, position=0, label="Call OI", ax=ax)
        pivot["PE"].plot(kind="bar", color="orange", width=0.4, position=1, label="Put OI", ax=ax)
        plt.title("NIFTY Open Interest Buildup (Nearest Expiry)")
        plt.xlabel("Strike Price")
        plt.ylabel("Open Interest")
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(fig)
    

    except Exception as e:
        st.error(f"❌ Failed to fetch instruments: {e}")

if __name__ == "__main__":
    main()
