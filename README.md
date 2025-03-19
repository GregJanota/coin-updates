# Coin Updates

A Python script that monitors cryptocurrency prices and sends email updates with price changes and trends.

## Features

- Monitors multiple cryptocurrencies simultaneously
- Sends HTML-formatted email updates with:
  - Current price
  - 24-hour price change
  - 7-day price change
  - 30-day price change
- Color-coded price changes (green for positive, red for negative)
- Configurable list of cryptocurrencies to monitor
- Uses CoinGecko API for real-time data

## Prerequisites

- Python 3.x
- Gmail account (or other SMTP server)
- Required Python packages:
  - requests
  - smtplib (built-in)

## Setup

1. Clone this repository
2. Set up the following environment variables:

```bash
# Email Configuration
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-specific-password
RECIPIENT_EMAIL=recipient@example.com

# Optional SMTP Configuration (defaults to Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Configure coins to monitor (choose one format)
# Format 1 - JSON array:
WATCHED_COINS='["bitcoin", "ethereum", "solana"]'
# Format 2 - Comma-separated:
WATCHED_COINS_LIST=bitcoin,ethereum,solana
```

### Gmail Setup

If using Gmail:
1. Enable 2-factor authentication
2. Generate an App Password:
   - Go to Google Account settings
   - Security
   - 2-Step Verification
   - App passwords
   - Generate a new app password for "Mail"
   - Use this password as your `EMAIL_PASS`

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Validate the configuration
2. Fetch current cryptocurrency data
3. Generate an HTML email with price updates
4. Send the email to the specified recipient

## Default Configuration

If no coins are specified in the environment variables, the script will monitor:
- Bitcoin (BTC)
- Ethereum (ETH)

## Error Handling

The script includes error handling for:
- Missing environment variables
- API request failures
- Email sending issues
- Invalid coin configurations

## Scheduling

To run this script automatically at regular intervals, you have several options:

### Heroku
1. Add a `Procfile` with:
   ```
   worker: python main.py
   ```
2. Add the Heroku Scheduler add-on to your app
3. Configure the scheduler to run at your desired frequency (e.g., every hour)
4. Set up your environment variables in Heroku's config vars

### Other Cloud Options
- **AWS Lambda**: Set up with CloudWatch Events/EventBridge for scheduled execution
- **Google Cloud Functions**: Use Cloud Scheduler to trigger the function
- **DigitalOcean**: Configure with their App Platform and Cron jobs
- **GitHub Actions**: Set up workflow with cron schedule

Remember that free-tier services may have limitations on execution frequency and uptime.

## License

This project is open source and available under the MIT License. 
