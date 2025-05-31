
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kiteconnect import KiteConnect
from matplotlib.gridspec import GridSpec

# -----------------------------
# 1. Zerodha API Configuration
# -----------------------------
API_KEY = os.getenv("Z_API_KEY")
ACCESS_TOKEN = os.getenv("Z_ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# -----------------------------
# 2. Fetch Instruments
# -----------------------------
def get_instruments():
    all_instruments = kite.instruments()
    df = pd.DataFrame(all_instruments)
    return df

# -----------------------------
# 3. Filter and Process OI Data
# -----------------------------
def fetch_oi_snapshot(df_instruments):
    df_opt = df_instruments[df_instruments["segment"] == "NFO-OPT"]
    df_opt = df_opt[df_opt["exchange"] == "NSE"]
    df_opt = df_opt[df_opt["instrument_type"].isin(["CE", "PE"])]

    # Filter for NIFTY and BANKNIFTY only
    df_nifty = df_opt[df_opt["name"] == "NIFTY"]
    df_banknifty = df_opt[df_opt["name"] == "BANKNIFTY"]

    return df_nifty, df_banknifty

# -----------------------------
# 4. Sample Visualization (Index OI)
# -----------------------------
def plot_oi_chart(df, title, color_ce, color_pe):
    weekly = df.groupby(["expiry", "instrument_type"])["open_interest"].sum().unstack()
    weekly = weekly.fillna(0).sort_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    weekly["CE"].plot(kind="bar", color=color_ce, position=0, width=0.4, label="CE", ax=ax)
    weekly["PE"].plot(kind="bar", color=color_pe, position=1, width=0.4, label="PE", ax=ax)
    plt.title(title)
    plt.xlabel("Expiry Date")
    plt.ylabel("Open Interest (Lakh)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    return fig

# -----------------------------
# 5. Generate Dashboard
# -----------------------------
def generate_dashboard():
    instruments_df = get_instruments()
    df_nifty, df_banknifty = fetch_oi_snapshot(instruments_df)

    # Example dashboard layout
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])
    plot_oi_chart(df_nifty, "NIFTY - Weekly OI (CE vs PE)", "gold", "navy").axes[0].get_figure().axes[0].set_position(ax1.get_position())
    ax2 = fig.add_subplot(gs[0, 1])
    plot_oi_chart(df_banknifty, "BANKNIFTY - Monthly OI (CE vs PE)", "green", "black").axes[0].get_figure().axes[0].set_position(ax2.get_position())

    # Placeholder for other charts (for now)
    fig.suptitle("Daily Derivatives InfoScape", fontsize=16)
    plt.tight_layout()
    fig.subplots_adjust(top=0.92)

    filename = f"daily_derivatives_dashboard_{datetime.date.today()}.png"
    plt.savefig(filename, dpi=300)
    print(f"✅ Dashboard saved as {filename}")

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    generate_dashboard()
