import os
import requests
from bs4 import BeautifulSoup
import csv
import datetime
import smtplib


def send_email():
  EMAIL = os.getenv("EMAIL")
  PASSWORD = os.getenv("EMAIL_PASSWORD")
  TO_EMAIL = os.getenv("TO_EMAIL")
  
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
  
  current price: 
  Happy purchase!
  """
  
  msg = f"Subject: {subject}\n\n{body}"
  
  server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  server.ehlo()
  server.login(EMAIL, PASSWORD)
  server.sendmail(from_addr=EMAIL, to_addrs=TO_EMAIL, msg=msg)
  server.quit()
  print("✅ Email sent successfully.")

url = r"https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZF1485D/ref=sr_1_13?crid=D6ZBLXYF6MZR&dib=eyJ2IjoiMSJ9.2IFLHkotYlL4BG4BUZf33JVCUcDkw7lossku0F_J22DDcAdtXjSR0VUbIx2_ccCjR56phumSBAYkL8oL3O7e8ppnX6aqBLfnFUzBSNa01vIGMqCzS2yL1V5RsxsZu4w5YW0tmcFUzMJY5g_WUdyiGlQNEbF1vu0q-0H6BuOJrZ3hlyjvFrrKy6FiIJdOfgQzjxyQg_gzpY9OZzSmcve1816GL796U_364LyroXlwaa4.UUAZ54Ypp4CBSoyu277X9WTQfhdVINFCwpnkyErOp4s&dib_tag=se&keywords=mac%2Bbook&qid=1757481962&sprefix=mac%2Bbo%2Caps%2C713&sr=8-13&th=1"

page = requests.get(url)
print(page)
  
  
  


