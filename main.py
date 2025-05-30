from data_fetcher import fetch_nifty_data
from chart_generator import plot_open_interest
from report_compiler import create_dashboard_image
from email_sender import send_email_with_attachment

def run():
    data = fetch_nifty_data()
    plot_open_interest(data)
    create_dashboard_image()
    send_email_with_attachment()

if __name__ == "__main__":
    run()