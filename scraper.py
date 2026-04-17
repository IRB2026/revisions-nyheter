import feedparser
import json
import os
from datetime import datetime

# Inställningar - Nu med korrelerad stavning: Cedra
FIRMS = ["BDO", "Grant Thornton", "Cedra"]
DATA_FILE = "news_history.json"

def fetch_news(firm):
    # Vi lägger till "revisionsbranschen" för att få mer relevanta träffar
    query = f"{firm}+revisionsbranschen"
    url = f"https://news.google.com/rss/search?q={query}+when:1d&hl=sv&gl=SE&ceid=SE:sv"
    feed = feedparser.parse(url)
    news_items = []
    
    for entry in feed.entries:
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "date": entry.published,
            "source": entry.source.title if hasattr(entry, 'source') else "Okänd",
            "firm": firm
        })
    return news_items

def update_database():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    for firm in FIRMS:
        new_news = fetch_news(firm)
        for item in new_news:
            if not any(h['link'] == item['link'] for h in history):
                history.append(item)

    # Sortera så nyast är först
    history.sort(key=lambda x: x['date'], reverse=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    update_database()
