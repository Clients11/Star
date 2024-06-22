import os
import requests
from pyrogram import Client, filters
from DAXXMUSIC import app

# Fetch the API key from environment variable for better security
news_api_key = os.getenv("NEWS_API_KEY", "44f2f0cfa39e4811ae305594d9b767d6")
news_base_url = "https://newsapi.org/v2/top-headlines"

def get_top_headlines(country="in", limit=5):
    try:
        response = requests.get(news_base_url, params={"apiKey": news_api_key, "country": country})
        response.raise_for_status()  # Raise an error for bad status codes
        news_data = response.json()

        if news_data["status"] != "ok":
            return "Failed to fetch news: API returned an error."

        articles = news_data.get("articles", [])
        if not articles:
            return "No news articles found."

        news_items = []
        for article in articles[:limit]:
            title = article.get("title", "No Title")
            description = article.get("description", "No Description")
            content = article.get("content", "No Content")
            news_items.append(f"Title: {title}\n\nDescription: {description}\n\nContent: {content}")

        return "\n\n".join(news_items)
    except requests.RequestException as e:
        return f"Failed to fetch news: {e}"
    except ValueError:
        return "Failed to parse news data."

@app.on_message(filters.command("news"))
def send_news(client, message):
    news = get_top_headlines()
    message.reply(news)
