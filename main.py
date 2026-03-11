from selenium import webdriver
from collections import Counter
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") 

def translate_text(text):

    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": text,
        "source": "es",
        "target": "en"
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = response.json()

    return result["data"
                  ]["translations"]["translatedText"]

def run_scraper(driver):

    # Create image folder
    if not os.path.exists("images"):
        os.makedirs("images")

    # Open opinion page
    driver.get("https://elpais.com/opinion/")
    time.sleep(5)

    # Get first 5 article links
    articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

    links = []

    for a in articles:
        link = a.get_attribute("href")
        if link and "/opinion/" in link and ".html" in link:
            links.append(link)

    links = links[:5]

    translated_titles = []

    for index, url in enumerate(links):

        if url:
            driver.get(url)
            time.sleep(4)

        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
            print("\nTITLE (Spanish):", title)

            translated = translate_text(title)
            print("TITLE (English):", translated)

            translated_titles.append(translated)

            paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")

            content = " ".join([p.text for p in paragraphs])

            print(f"\nCONTENT:\n{content}\n")

        except Exception as e:
            print("Error loading article", e)
            continue

        try:
            image = driver.find_element(By.CSS_SELECTOR, "figure img")
            img_url = image.get_attribute("src")

            img_data = requests.get(img_url).content

            with open(f"images/article_{index+1}.jpg", "wb") as f:
                f.write(img_data)

            print("Image saved: article_", index+1)

        except:
            print("No image found")

    print("\nAll Translated Titles:")
    print(translated_titles)

    words = []

    for title in translated_titles:
        words.extend(title[0].lower().split())

    counter = Counter(words)

    print("\nRepeated Words (occurring more than twice):")

    for word, count in counter.items():
        if count > 2:
            print(word, ":", count)
