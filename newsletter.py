import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Sender Gmail address
sender_email = "siegerintern@gmail.com"

# App Password from GitHub secret
app_password = os.environ.get("APP_PASSWORD")

# Recipients
recipients = [sender_email]

# Specialized RSS feeds
rss_urls = [
    "https://www.parking.net/rss",
    "https://www.automation.com/rss-feeds/news",
    "https://www.smartcitiesworld.net/rss/news",
    "https://www.mmh.com/rss",
    "https://www.supplychainquarterly.com/rss",
    "https://www.textileworld.com/feed/",
    "https://www.fibre2fashion.com/rss/news.aspx?type=industry"
]

# Keywords to filter
keywords = [
    "car parking",
    "automated parking",
    "parking system",
    "warehouse automation",
    "automated warehouse",
    "warehouse robotics",
    "textile machinery",
    "spinning machine",
    "weaving",
    "automation",
    "logistics automation",
    "storage solutions",
    "robotic system"
]

# Fetch and filter news
html_content = """
<h2>📰 Daily Industry Automation & Textile News</h2>
<ul>
"""

filtered_count = 0

for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        combined_text = (entry.title + entry.get("summary", "")).lower()
        if any(keyword in combined_text for keyword in keywords):
            html_content += f'<li><a href="{entry.link}">{entry.title}</a></li>'
            filtered_count += 1

html_content += "</ul>"

if filtered_count == 0:
    html_content += "<p>No relevant articles found today.</p>"

html_content += "<hr><p>This is an automated email sent from GitHub Actions.</p>"

# Compose email
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = ", ".join(recipients)
msg["Subject"] = "Daily Automation & Textile Newsletter"

msg.attach(MIMEText(html_content, "html"))

# Send email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, recipients, msg.as_string())
    server.quit()
    print("✅ Filtered newsletter sent successfully!")
except Exception as e:
    print("❌ Error:", e)
