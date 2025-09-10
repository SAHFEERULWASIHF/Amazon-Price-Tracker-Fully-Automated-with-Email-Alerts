import base64
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from github import Github, Auth
import smtplib
import io
import re

# -------------------- CONFIG --------------------
GITHUB_TOKEN = os.getenv("PUBLIC_REPO_TOKEN")
REPO_NAME = "SAHFEERULWASIHF/Amazon-MacBook-Price-Tracker"
FILE_PATH = "amezonWebScrapping/Amezon_web_Scraping_Project.csv"
BRANCH = "main"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
PRICE_THRESHOLD = 130000

URL = "https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZF1485D/ref=sr_1_13?crid=D6ZBLXYF6MZR&dib=eyJ2IjoiMSJ9.2IFLHkotYlL4BG4BUZf33JVCUcDkw7lossku0F_J22DDcAdtXjSR0VUbIx2_ccCjR56phumSBAYkL8oL3O7e8ppnX6aqBLfnFUzBSNa01vIGMqCzS2yL1V5RsxsZu4w5YW0tmcFUzMJY5g_WUdyiGlQNEbF1vu0q-0H6BuOJrZ3hlyjvFrrKy6FiIJdOfgQzjxyQg_gzpY9OZzSmcve1816GL796U_364LyroXlwaa4.UUAZ54Ypp4CBSoyu277X9WTQfhdVINFCwpnkyErOp4s&dib_tag=se&keywords=mac%2Bbook&qid=1757481962&sprefix=mac%2Bbo%2Caps%2C713&sr=8-13&th=1"

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/"
}

# -------------------- FUNCTIONS --------------------
def send_mail(current_price):
    subject = "MacBook is on sale! - My Project"
    body = f"""Dear me!,
    
The MacBook you were waiting for is now on sale.  
When I started this project, the prices were:
    
- Black and Sky Blue, 512GB hard disk, 24GB RAM - 125k  
- White and Off White, 512GB, 24GB RAM - 135k  
- All colors, 256GB hard disk, 16GB RAM - 84k  
    
I'm waiting for it to go under 100k to buy. Now it must be under 1 lakh to end up in this mail.  
Go buy this!  
    
The link I used for web scraping must still work. Try the link:  
{URL}

current price: {current_price}
Happy purchase!
"""
    msg = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(EMAIL, PASSWORD)
        server.sendmail(from_addr=EMAIL, to_addrs=TO_EMAIL, msg=msg)
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def get_github_csv():
    """Fetch CSV + sha if exists, else return empty DataFrame"""
    g = Github(auth=Auth.Token(GITHUB_TOKEN))
    repo = g.get_repo(REPO_NAME)

    try:
        contents = repo.get_contents(FILE_PATH, ref=BRANCH)
        csv_data = base64.b64decode(contents.content).decode("utf-8")
        df = pd.read_csv(io.StringIO(csv_data))
        return df, contents.sha, repo
    except Exception as e:
        print("⚠️ No file found, will create new one:", e)
        return pd.DataFrame(columns=["Name", "Price", "Date"]), None, repo


def update_github_csv(df, sha, repo):
    """Update or create CSV file in repo"""
    content = df.to_csv(index=False)

    try:
        if sha:  # file exists → update
            repo.update_file(
                path=FILE_PATH,
                message="Update price log",
                content=content,
                sha=sha,
                branch=BRANCH,
            )
            print("✅ CSV updated on GitHub")
        else:
            # double-check: if file actually exists, fetch sha again
            try:
                contents = repo.get_contents(FILE_PATH, ref=BRANCH)
                repo.update_file(
                    path=FILE_PATH,
                    message="Update price log (retry)",
                    content=content,
                    sha=contents.sha,
                    branch=BRANCH,
                )
                print("✅ CSV updated on GitHub (retry)")
            except Exception:
                repo.create_file(
                    path=FILE_PATH,
                    message="Create price log",
                    content=content,
                    branch=BRANCH,
                )
                print("✅ CSV created on GitHub")
    except Exception as e:
        print("❌ GitHub update failed:", e)

def check_price():
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")

    # Scrape product title
    name_soup = soup.find(id="productTitle")
    if not name_soup:
        print("❌ Product title not found")
        return
    name = name_soup.get_text(strip=True)

    # Scrape price
    price_soup = soup.find(class_ = 'aok-offscreen')
    if not price_soup:
        print("❌ Price not found")
        return
    price_text = price_soup.get_text(strip=True).replace("₹","").replace(",","")
    price_text = re.sub(r'[A-Za-z]', '', price_text)
    price_text = price_text.split(' ')[0]
    current_price = int(float(price_text))

    # Append to GitHub CSV
    df, sha, repo = get_github_csv()
    today = datetime.date.today()
    df = pd.concat([df, pd.DataFrame([{"Name": name, "Price": current_price, "Date": today}])], ignore_index=True)
    update_github_csv(df, sha, repo)

    print(f"✅ Price logged: ₹{current_price}")

    # Send email if price is below threshold
    if current_price < PRICE_THRESHOLD:
        send_mail(current_price-30000)

# -------------------- RUN --------------------
if __name__ == "__main__":
    check_price()



