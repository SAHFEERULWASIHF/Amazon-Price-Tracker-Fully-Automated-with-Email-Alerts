import os
import requests
from bs4 import BeautifulSoup
import csv
import datetime
import smtplib

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('EMAIL_PASSWORD') 
TO_EMAIL = os.getenv('TO_EMAIL') 
PRICE_THRESHOLD = 100000 
CSV_FILE = r"amezonWebScrapping/Amezon_web_Scraping_Project.csv"

URL = r"https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZF1485D/ref=sr_1_13?crid=D6ZBLXYF6MZR&dib=eyJ2IjoiMSJ9.2IFLHkotYlL4BG4BUZf33JVCUcDkw7lossku0F_J22DDcAdtXjSR0VUbIx2_ccCjR56phumSBAYkL8oL3O7e8ppnX6aqBLfnFUzBSNa01vIGMqCzS2yL1V5RsxsZu4w5YW0tmcFUzMJY5g_WUdyiGlQNEbF1vu0q-0H6BuOJrZ3hlyjvFrrKy6FiIJdOfgQzjxyQg_gzpY9OZzSmcve1816GL796U_364LyroXlwaa4.UUAZ54Ypp4CBSoyu277X9WTQfhdVINFCwpnkyErOp4s&dib_tag=se&keywords=mac%2Bbook&qid=1757481962&sprefix=mac%2Bbo%2Caps%2C713&sr=8-13&th=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.7204.185 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# --- Functions ---
def send_mail(current_price):
    subject = "MacBook is on sale! - My Project results"
    body = f"""Dear me!,
    
The MacBook you were waiting for is now on sale.  
When I started this project, the prices were:
    
- Black and Sky Blue, 512GB hard disk, 24GB RAM - 125k  
- White and Off White, 512GB, 24GB RAM - 135k  
- All colors, 256GB hard disk, 16GB RAM - 84k  
    
I'm waiting for it to go under 100k to buy. Now it must be under 1 lakh to end up in this mail.  
Go buy this!  
    
The link I used for web scraping must still work. Try the link:  
{url}

current price: {curr_price}
Happy purchase!
"""

    msg = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL, PASSWORD)
        server.sendmail(from_addr=EMAIL, to_addrs=TO_EMAIL, msg=msg)
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def check_price():
    try:
        page = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(page.content,'html.parser')

        # Get product title
        name_soup = soup.find(id = 'productTitle')
        if not name_soup:
            print("❌ Product title not found")
            return
        name = name_soup.text.strip()

        # Get price
        # Try multiple selectors for price
        price_soup = soup.select_one("span.a-price .a-offscreen") \
                        or soup.select_one("span.a-price-whole")

        if not price_soup:
            print("❌ Price not found")
            return
        
        price_text = price_soup.get_text(strip=True)
        # Remove currency and commas
        price_text = price_text.replace("₹", "").replace(",", "").replace(".","")
        current_price = int("".join(filter(str.isdigit, price_text)))


        # Log to CSV
        date_str = datetime.date.today()
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Name', 'Price', 'Date'])
            writer.writerow([name, current_price, date_str])
        print(f"✅ Logged price: ₹{current_price}")

        # Send email if price is below threshold
        if current_price < PRICE_THRESHOLD:
            send_mail(current_price)

    except Exception as e:
        print(f"❌ Error checking price: {e}")


# --- Run ---
if __name__ == "__main__":
    check_price()



