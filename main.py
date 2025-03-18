import smtplib
import requests
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
from datetime import datetime

# Email configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

def get_watched_coins():
    """
    Get watched coins from environment variables.
    Supports two formats:
    1. JSON array: WATCHED_COINS='["bitcoin", "ethereum"]'
    2. Comma-separated: WATCHED_COINS_LIST='bitcoin,ethereum,solana'
    """
    # Try JSON format first
    json_coins = os.getenv('WATCHED_COINS')
    if json_coins:
        try:
            return json.loads(json_coins)
        except json.JSONDecodeError:
            print("Warning: WATCHED_COINS is not valid JSON, trying WATCHED_COINS_LIST")
    
    # Try comma-separated format
    coins_list = os.getenv('WATCHED_COINS_LIST')
    if coins_list:
        # Split by comma and strip whitespace
        return [coin.strip() for coin in coins_list.split(',')]
    
    # Default coins if nothing is configured
    return ["bitcoin", "ethereum"]

# Get the watched coins
WATCHED_COINS = get_watched_coins()

def fetch_crypto_data(coin_ids: List[str]) -> dict:
    coins_param = ",".join(coin_ids)
    
    base_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": coins_param,
        "order": "market_cap_desc",
        "per_page": len(coin_ids),
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h,7d,30d"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def format_percentage(value):
    if value is None or value == 'N/A':
        return 'N/A'
    color = 'green' if value > 0 else 'red'
    return f'<span style="color: {color}">{value:.1f}%</span>'

def create_crypto_email_body(coins_data):
    html_body = "<html><body>"
    
    # Create a dictionary for O(1) lookup of coin data
    coins_dict = {coin['id']: coin for coin in coins_data}
    
    # Use the original WATCHED_COINS order to display coins
    for coin_id in WATCHED_COINS:
        try:
            coin = coins_dict[coin_id]
            html_body += f"""
            <p><b>{coin['id'].upper()}</b>:
            <br>Current Price: ${coin['current_price']:,.2f}
            <br>24h Change: {format_percentage(coin.get('price_change_percentage_24h_in_currency'))}
            <br>7d Change: {format_percentage(coin.get('price_change_percentage_7d_in_currency'))}
            <br>30d Change: {format_percentage(coin.get('price_change_percentage_30d_in_currency'))}
            </p>"""
        except KeyError as e:
            html_body += f"<p>Error accessing data for {coin_id}: {e}</p>"
    
    html_body += "</body></html>"
    return html_body

def send_email(subject, body, sender, recipient, is_html=False):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html" if is_html else "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def send_crypto_update():
    """
    Fetch crypto data and send an email update for the specified coins
    """
    try:
        print(f"Sending crypto update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        crypto_data = fetch_crypto_data(WATCHED_COINS)
        
        if crypto_data:
            email_body = create_crypto_email_body(crypto_data)
            
            send_email(
                subject="Crypto Currency Update",
                body=email_body,
                sender=EMAIL_USER,
                recipient=RECIPIENT_EMAIL,
                is_html=True
            )
            print("Email sent successfully!")
            return True
        else:
            print("No crypto data received")
            return False
    except Exception as e:
        print(f"Error in send_crypto_update: {e}")
        return False

def validate_config():
    """
    Validate that all required environment variables are set
    """
    required_vars = {
        'EMAIL_USER': EMAIL_USER,
        'EMAIL_PASS': EMAIL_PASS,
        'RECIPIENT_EMAIL': RECIPIENT_EMAIL,
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    if not WATCHED_COINS:
        raise ValueError("No coins configured to watch")
    
    print(f"Configuration validated. Watching coins: {', '.join(WATCHED_COINS)}")

if __name__ == "__main__":
    validate_config()
    send_crypto_update()