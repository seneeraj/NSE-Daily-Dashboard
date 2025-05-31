from data_fetcher import fetch_nifty_data
from chart_generator import plot_open_interest
from emailer import send_email  # if using

def run():
    data = fetch_nifty_data()
    if data:
        plot_open_interest(data)
        # send_email(...)  # optional step
    else:
        print("No data received.")

   
if __name__ == "__main__":
    run()
