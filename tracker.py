import os
import requests
import smtplib

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

print(EMAIL)

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

{EMAIL},
{PASSWORD}
"""

msg = f"Subject: {subject}\n\n{body}"

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(EMAIL, PASSWORD)
server.sendmail(from_addr=EMAIL, to_addrs=TO_EMAIL, msg=msg)
server.quit()
print("✅ Email sent successfully.")













