from data_fetcher import fetch_nifty_data
from chart_generator import plot_open_interest

def run():
    data = fetch_nifty_data()
    if data:
        plot_open_interest(data)
    else:
        print("❌ No data to plot.")

if __name__ == "__main__":
    run()
