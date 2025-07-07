import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# RSS feeds
feeds = [
    "https://www.mmh.com/rss/topic/11541",
    "https://logisticsviewpoints.com/feed/",
    "https://www.parking.net/rss",
    "https://www.textileworld.com/feed/"
]

# Keywords to filter
keywords = [
    "automation",
    "automated",
    "warehouse automation",
    "car parking automation",
    "textile automation"
]

# Recipients
recipients = [
    "siegerintern@gmail.com",
    "kavyaraj922@gmail.com"
]

# Sender credentials
sender_email = os.environ["SENDER_EMAIL"]
app_password = os.environ["APP_PASSWORD"]

# Collect relevant articles
articles = []

for url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.title.lower()
        summary = entry.summary.lower() if "summary" in entry else ""
        if any(keyword in title or keyword in summary for keyword in keywords):
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if "published" in entry else "No date"
            })

if not articles:
    print("No relevant articles found.")
    exit()

# Create HTML email
html = """
<h2>Daily Automation News Digest</h2>
<ul>
"""
for article in articles:
    html += f"<li><a href='{article['link']}'>{article['title']}</a> - {article['published']}</li>"
html += "</ul>"

# Email setup
msg = MIMEMultipart("alternative")
msg["Subject"] = "Daily Automation News Digest"
msg["From"] = sender_email
msg["To"] = ", ".join(recipients)
part = MIMEText(html, "html")
msg.attach(part)

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, app_password)
    server.sendmail(sender_email, recipients, msg.as_string())

print("Newsletter sent successfully.")
