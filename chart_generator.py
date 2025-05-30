import matplotlib.pyplot as plt

def plot_open_interest(data):
    ce_oi = []
    pe_oi = []
    strikes = []

    for item in data['records']['data']:
        strike = item['strikePrice']
        if 'CE' in item and 'PE' in item:
            ce_oi.append(item['CE']['openInterest'])
            pe_oi.append(item['PE']['openInterest'])
            strikes.append(strike)

    plt.figure(figsize=(10,5))
    plt.bar(strikes, ce_oi, width=40, label="Call OI", color='skyblue')
    plt.bar(strikes, pe_oi, width=40, label="Put OI", color='orange', alpha=0.7)
    plt.xlabel("Strike Price")
    plt.ylabel("Open Interest")
    plt.legend()
    plt.title("Nifty Open Interest - CE vs PE")
    plt.tight_layout()
    plt.savefig("nifty_oi.png")