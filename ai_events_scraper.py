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
    data = (
        scrape_eventbrite() +
        scrape_kaggle() +
        scrape_mlconf() +
        scrape_google_ai() +
        scrape_meetup() +
        scrape_devpost()
    )
    df = pd.DataFrame(data)
    st.success("✅ Scraped successfully!")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv, "ai_ml_opportunities.csv", "text/csv")

    st.markdown("### 📋 Copy this for email (or paste into Gmail)")
    st.code(df.to_markdown(index=False), language="markdown")
