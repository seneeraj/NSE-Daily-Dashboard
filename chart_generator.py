import matplotlib.pyplot as plt

def plot_open_interest(data):
    ce_oi = []
    pe_oi = []
    strikes = []

    for item in data:
        if 'CE' in item and 'PE' in item:
            strikes.append(item['strikePrice'])
            ce_oi.append(item['CE']['openInterest'])
            pe_oi.append(item['PE']['openInterest'])

    if not strikes:
        print("⚠️ No valid option chain data found.")
        return

    plt.figure(figsize=(12, 6))
    plt.bar(strikes, ce_oi, width=20, label='Call OI', color='green')
    plt.bar(strikes, pe_oi, width=10, label='Put OI', color='red', alpha=0.7)
    plt.xlabel("Strike Price")
    plt.ylabel("Open Interest")
    plt.title("NIFTY Option Chain - Open Interest")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("nifty_oi_chart.png")
    plt.close()
    print("✅ Chart saved as nifty_oi_chart.png")
