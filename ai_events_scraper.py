import feedparser  
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI/ML Opportunities", layout="wide")
st.title("🧠 AI/ML Events & Opportunities Scraper")

@st.cache_data
def scrape_eventbrite():
    url = "https://www.eventbrite.com/d/online/artificial-intelligence/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    events = []
    for card in soup.select('div.eds-event-card-content__content'):
        title = card.select_one('div.eds-event-card-content__primary-content').get_text(strip=True)
        link = card.find_parent('a')['href']
        date = card.select_one('div.eds-text-bs--fixed').get_text(strip=True)
        events.append({
            'Title': title,
            'Date': date,
            'Link': link,
            'Source': 'Eventbrite'
        })
    return events

@st.cache_data
def scrape_kaggle():
    url = "https://www.kaggle.com/competitions"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    contests = []
    for div in soup.select('div.sc-dEvZhu'):
        title_tag = div.select_one('a.sc-jUosCB')
        if title_tag:
            title = title_tag.text.strip()
            link = "https://kaggle.com" + title_tag['href']
            contests.append({
                'Title': title,
                'Date': 'Ongoing',
                'Link': link,
                'Source': 'Kaggle'
            })
    return contests

def scrape_mlconf():
    return [{'Title': 'MLConf 2025', 'Date': 'TBD', 'Link': 'https://mlconf.com', 'Source': 'MLConf'}]

def scrape_google_ai():
    return [{'Title': 'Google AI Courses', 'Date': '-', 'Link': 'https://ai.google/education/', 'Source': 'Google AI'}]

def scrape_meetup():
    return [{'Title': 'AI Meetup NYC', 'Date': 'Check site', 'Link': 'https://meetup.com', 'Source': 'Meetup'}]

def scrape_devpost():
    return [{'Title': 'AI Hackathon on Devpost', 'Date': 'Open', 'Link': 'https://devpost.com/hackathons', 'Source': 'Devpost'}]

if st.button("🔍 Scrape Now"):
    all_sources = []
    with st.spinner("Scraping sources..."):
        for func in [
            scrape_eventbrite,
            scrape_kaggle,
            scrape_mlconf,
            scrape_google_ai,
            scrape_meetup,
            scrape_devpost,
            scrape_ai_expo,
            scrape_paperswithcode,
            scrape_ai_weekly,
            scrape_arxiv_ml,
        ]:
            try:
                all_sources.extend(func())
            except Exception as e:
                st.warning(f"⚠️ {func.__name__} failed: {e}")

    df = pd.DataFrame(all_sources)
    st.success("✅ Scraped successfully!")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv, "ai_ml_opportunities.csv", "text/csv")

    st.markdown("### 📋 Copy this for email (or paste into Gmail)")
    st.code(df.to_markdown(index=False), language="markdown")


def scrape_ai_expo():
    url = "https://www.ai-expo.net/global/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    events = []
    for item in soup.select('div.event-post'):
        title_tag = item.select_one("h4")
        link_tag = item.select_one("a")
        date_tag = item.select_one("div.date")

        if title_tag and link_tag:
            events.append({
                'Title': title_tag.get_text(strip=True),
                'Date': date_tag.get_text(strip=True) if date_tag else '-',
                'Link': link_tag['href'],
                'Source': 'AI Expo'
            })
    return events

def scrape_paperswithcode():
    url = "https://paperswithcode.com/trending"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    papers = []
    for paper in soup.select("div.paper-card"):
        title_tag = paper.select_one("h1.paper-title a")
        if title_tag:
            papers.append({
                'Title': title_tag.get_text(strip=True),
                'Date': '-',  # No date available
                'Link': "https://paperswithcode.com" + title_tag['href'],
                'Source': 'PapersWithCode'
            })
    return papers

def scrape_ai_weekly():
    url = "https://aiweekly.co/issues"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    issues = []
    for issue in soup.select("div.issue-list li"):
        link = issue.select_one("a")
        if link:
            issues.append({
                'Title': link.get_text(strip=True),
                'Date': '-',  # Optional: extract date from text
                'Link': link['href'],
                'Source': 'AI Weekly'
            })
    return issues

def scrape_arxiv_ml():
    feed_url = "http://export.arxiv.org/rss/cs.LG"  # Machine Learning RSS
    feed = feedparser.parse(feed_url)

    entries = []
    for entry in feed.entries[:10]:
        entries.append({
            'Title': entry.title,
            'Date': entry.published,
            'Link': entry.link,
            'Source': 'arXiv ML'
        })
    return entries
