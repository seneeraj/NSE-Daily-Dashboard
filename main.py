import streamlit as st
from data_fetcher import fetch_nifty_data
from chart_generator import plot_open_interest
import os

def run():
    st.title("📊 NIFTY Open Interest Chart (Daily)")
    
    data = fetch_nifty_data()
    if data:
        plot_open_interest(data)
        if os.path.exists("nifty_oi_chart.png"):
            st.image("nifty_oi_chart.png", caption="NIFTY OI Chart", use_column_width=True)
        else:
            st.error("⚠️ Chart image not found.")
    else:
        st.error("❌ Failed to fetch or parse NIFTY option chain data.")

if __name__ == "__main__":
    run()
