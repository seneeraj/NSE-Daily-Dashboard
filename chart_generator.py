import matplotlib.pyplot as plt

def plot_open_interest(data):
    strike_prices = []
    ce_oi = []
    pe_oi = []

    for item in data:
        if 'CE' in item and 'PE' in item:
            strike_prices.append(item['strikePrice'])
            ce_oi.append(item['CE']['openInterest'])
            pe_oi.append(item['PE']['openInterest'])

    plt.figure(figsize=(10, 5))
    plt.bar(strike_prices, ce_oi, width=20, label='Call OI', color='skyblue')
    plt.bar(strike_prices, pe_oi, width=10, label='Put OI', color='orange', alpha=0.7)
    plt.xlabel("Strike Price")
    plt.ylabel("Open Interest")
    plt.title("Nifty Option Chain - Open Interest")
    plt.legend()
    plt.tight_layout()
    plt.savefig("nifty_oi_chart.png")
    plt.close()
