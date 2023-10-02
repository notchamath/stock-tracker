import requests
import os
from dotenv import load_dotenv

# Stock Details
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Allowed change in %
ALLOWED_PERCENTAGE_CHANGE = 5

# API Endpoints
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Load env file
load_dotenv('.env')

# Get Environment Variables
STOCK_KEY = os.getenv("STOCK_KEY")
NEWS_KEY = os.getenv("NEWS_KEY")


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price.

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_KEY,
}
res = requests.get(STOCK_ENDPOINT, params=params)
res.raise_for_status()

data = res.json()["Time Series (Daily)"]
keys = list(data.keys())[1:3]

price_yest = float(data[keys[0]]["4. close"])
price_prev = float(data[keys[1]]["4. close"])

price_change = round(price_prev - price_yest, 2)
price_change_percentage = round((price_change/price_yest) * 100)

get_news = False
if abs(price_change_percentage) >= ALLOWED_PERCENTAGE_CHANGE:
    get_news = True

## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
#HINT 1: Think about using the Python Slice Operator

if get_news:
    params = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_KEY,
        "sortBy": "publishedAt",
        "pageSize": 3,
    }
    res = requests.get(NEWS_ENDPOINT, params=params)
    res.raise_for_status()

    news = res.json()["articles"]

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number.
#HINT 1: Consider using a List Comprehension.
    for article in news:
        emoji = "🔺"
        if price_change_percentage < 0:
            emoji = "🔻"

        msg = f"""
            {STOCK}: {emoji} {price_change_percentage}%
            Headline: {article["title"]}
            Brief: {article["description"]}
            URL: {article["url"]}
        """
        print(msg)
