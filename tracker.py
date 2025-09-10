import smtplib
import os

def send_mail(curr_price):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(EMAIL, PASSWORD)
    
    subject = "MacBook is in sale - my prject call"
    body = f"""Dear me!,
    
The MacBook you were waiting for is now on sale.  
When I started this project, the prices were:
    
- Black and Sky Blue, 512GB hard disk, 24GB RAM - 125k  
- White and Off White, 512GB, 24GB RAM - 135k  
- All colors, 256GB hard disk, 16GB RAM - 84k  
    
I'm waiting for it to go under 100k to buy. Now it must be under 1 lakh to end up in this mail.  
Go buy this!  
    
The link I used for web scraping must still work. Try the link:  
https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZF1485D/ref=sr_1_13?crid=D6ZBLXYF6MZR&dib=eyJ2IjoiMSJ9.2IFLHkotYlL4BG4BUZf33JVCUcDkw7lossku0F_J22DDcAdtXjSR0VUbIx2_ccCjR56phumSBAYkL8oL3O7e8ppnX6aqBLfnFUzBSNa01vIGMqCzS2yL1V5RsxsZu4w5YW0tmcFUzMJY5g_WUdyiGlQNEbF1vu0q-0H6BuOJrZ3hlyjvFrrKy6FiIJdOfgQzjxyQg_gzpY9OZzSmcve1816GL796U_364LyroXlwaa4.UUAZ54Ypp4CBSoyu277X9WTQfhdVINFCwpnkyErOp4s&dib_tag=se&keywords=mac%2Bbook&qid=1757481962&sprefix=mac%2Bbo%2Caps%2C713&sr=8-13&th=1

current price: {curr_price}
Happy purchase!
"""
    
    
    msg = f"subject: {subject}\n\n{body}"
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('EMAIL_PASSWORD')
    TO_EMAIL = os.getenv('TO_EMAIL')
    
    server.sendmail(from_addr=EMAIL, to_addrs=TO_EMAIL, msg=msg)

# mail function is loaded on top

import requests 
from bs4 import BeautifulSoup 
    
def check_price(i): 
    
    url = r"https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZF1485D/ref=sr_1_13?crid=D6ZBLXYF6MZR&dib=eyJ2IjoiMSJ9.2IFLHkotYlL4BG4BUZf33JVCUcDkw7lossku0F_J22DDcAdtXjSR0VUbIx2_ccCjR56phumSBAYkL8oL3O7e8ppnX6aqBLfnFUzBSNa01vIGMqCzS2yL1V5RsxsZu4w5YW0tmcFUzMJY5g_WUdyiGlQNEbF1vu0q-0H6BuOJrZ3hlyjvFrrKy6FiIJdOfgQzjxyQg_gzpY9OZzSmcve1816GL796U_364LyroXlwaa4.UUAZ54Ypp4CBSoyu277X9WTQfhdVINFCwpnkyErOp4s&dib_tag=se&keywords=mac%2Bbook&qid=1757481962&sprefix=mac%2Bbo%2Caps%2C713&sr=8-13&th=1"
    my_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/138.0.7204.185 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    page = requests.get(url, headers=my_headers)
    
    soup = BeautifulSoup(page.content,'html.parser') 
    
    price_soup = soup.find(class_ = 'a-price-whole')
    price = price_soup.text.strip(".")
    
    name_soup = soup.find(id = 'productTitle')
    name = name_soup.text.strip()
    
    import datetime
    day = datetime.date.today()
    
    if not os.path.exists(r"amezonWebScrapping"):
        os.mkdir("amezonWebScrapping")
        print('amezonWebScrapping folder created successfully!')
    
    file_exists = os.path.isfile(r"amezonWebScrapping/Amezon_web_Scraping_Project.csv")
    
    import csv
    
    with open('amezonWebScrapping/Amezon_web_Scraping_Project.csv','a',newline='', encoding='UTF8') as f:
        
        writer = csv.writer(f)
        
        if not file_exists: 
            writer.writerow(['Name','Price','Date'])
            print('csv file not existed before.\ncsv file created with headers succesfully!')
        writer.writerow([name, price, day])
        print(f'{i} - Data appended successfully')

    int_price = int(price.replace(",",""))

    if int_price < 100000: 
        send_mail(price)

import time

data_appended = 1

while(True): 
    check_price(data_appended)
    data_appended += 1

    time.sleep(60*60*24)
