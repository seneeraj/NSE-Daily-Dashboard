from PIL import Image

def create_dashboard_image():
    img = Image.open("nifty_oi.png")
    img.save("dashboard_report.png")