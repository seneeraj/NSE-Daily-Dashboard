import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import matplotlib.pyplot as plt
import time

# Set page config as the first Streamlit command
st.set_page_config(page_title="Zerodha Option Chain with OI Chart", layout="wide")

# Debugging: Display secrets to verify
st.write("✅ Secrets loaded:", st.secrets["zerodha"])

# Button to clear cache
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.write("Cache cleared!")

# 1. Initialize KiteConnect
def get_kite():
    api_key = st.secrets["zerodha"]["api_key"]
    access_token = st.secrets["zerodha"]["access_token"]
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite

# 2. Fetch instruments and cache them
@st.cache_data(show_spinner="Fetching instruments from Zerodha...")
def get_instruments(_kite):
    instruments = _kite.instruments()
    return pd.DataFrame(instruments)

# 3. Fetch OI using live quote API
def fetch_oi_data(kite, df, batch_size=50):
    tokens = df['instrument_token'].tolist()
    st.write(f"📊 Total tokens to process: {len(tokens)}")
    
    if not tokens:
        st.error("No tokens found in DataFrame!")
        return df

    oi_data = {}
    for i in range(0, len(tokens), batch_size):
        batch_tokens = tokens[i:i + batch_size]
        st.write(f"Processing batch {i//batch_size + 1} with {len(batch_tokens)} tokens")
        try:
            quotes = kite.quote(batch_tokens)
            oi_data.update(quotes)
            time.sleep(0.2)  # Avoid rate limits
        except Exception as e:
            st.warning(f"Error fetching batch {i//batch_size + 1}: {e}")
    
    # Add OI to DataFrame
    df['open_interest'] = df['instrument_token'].apply(lambda x: oi_data.get(str(x), {}).get("oi", 0))
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
        # Test API authentication
        st.write("🔍 Testing API authentication...")
        try:
            profile = kite.profile()
            st.write("✅ API authentication successful:", profile["user_name"])
        except Exception as e:
            st.error(f"❌ Authentication failed: {e}")
            st.info("Please regenerate the access token using the KiteConnect login flow: "
                    "1. Visit https://kite.trade/connect/login?api_key=your_api_key\n"
                    "2. Log in and get the request_token from the redirect URL\n"
                    "3. Use the request_token to generate a new access_token\n"
                    "4. Update st.secrets with the new access_token")
            return  # Stop execution if authentication fails

        df_all = get_instruments(kite)

        # Filter NIFTY options and limit to nearest expiry
        df_nifty = df_all[(df_all['name'] == 'NIFTY') & (df_all['segment'] == 'NFO-OPT')]
        if not df_nifty.empty:
            nearest_expiry = df_nifty['expiry'].min()
            df_nifty = df_nifty[df_nifty['expiry'] == nearest_expiry]
            st.write(f"📅 Nearest expiry date: {nearest_expiry}")
            df_nifty = df_nifty[df_nifty['strike'].between(df_nifty['strike'].quantile(0.1), df_nifty['strike'].quantile(0.9))]
        
        st.write(f"📊 Total NIFTY options after filtering: {len(df_nifty)}")

        st.subheader("📈 NIFTY Option Chain (Top 20)")
        st.dataframe(df_nifty.head(20))

        st.subheader("📊 OI Buildup Chart")
        df_nifty = fetch_oi_data(kite, df_nifty, batch_size=50)
        plot_oi_chart(df_nifty)

    except Exception as e:
        st.error(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
