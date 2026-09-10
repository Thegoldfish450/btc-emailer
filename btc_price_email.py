import os
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime

# --- Get BTC price from CoinGecko (free, no API key needed) ---
resp = requests.get(
    "https://api.coingecko.com/api/v3/simple/price",
    params={"ids": "bitcoin", "vs_currencies": "usd"},
    timeout=10,
)
resp.raise_for_status()
price = resp.json()["bitcoin"]["usd"]

# --- Build the email ---
today = datetime.now().strftime("%B %d, %Y")
subject = f"BTC Price — ${price:,.2f}"
body = f"Bitcoin price on {today}: ${price:,.2f} USD"

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = os.environ["GMAIL_ADDRESS"]
msg["To"] = os.environ["TO_EMAIL"]

# --- Send via Gmail SMTP ---
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(os.environ["GMAIL_ADDRESS"], os.environ["GMAIL_APP_PASSWORD"])
    server.send_message(msg)

print("Email sent:", subject)
