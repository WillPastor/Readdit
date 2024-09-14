import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Base URL of the Reddit-like site
BASE_URL = 'https://reddit-like-site.com'

# Set up Selenium with Chrome WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode (no UI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Hide automation signature
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Function to fetch posts from a page using Selenium with simulated scrolling
def fetch_posts(driver, url, limit, max_scroll_attempts=2):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    posts_collected = []
    
    last_height = driver.execute_script("return document.body.scrollHeight")  # Get initial scroll height
    previous_post_count = 0
    scroll_attempts = 0

    while len(posts_collected) < limit and scroll_attempts < max_scroll_attempts:
        # DEBUG: Print current page URL
        print(f"Current page URL: {driver.current_url}")
        
        # Find articles that represent each post
        articles = driver.find_elements(By.CSS_SELECTOR, 'article')  # Updated selector for articles
        
        print(f"Found {len(articles)} articles on this scroll.")

        for article in articles:
            if len(posts_collected) >= limit:
                break
            try:
                # Find the title of the post
                title = article.get_attribute('aria-label')  # Extract the aria-label attribute which holds the title
                print(f"Post Title: {title}")
                
                # Get the permalink for the post
                permalink = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                print(f"Post Permalink: {permalink}")

                # Extract the votes if available (assuming it's in a span or similar tag, update if necessary)
                votes = article.find_element(By.CSS_SELECTOR, 'shreddit-post').get_attribute('score')
                
                # Append the collected post data
                posts_collected.append({
                    'title': title,
                    'link': permalink,
                    'votes': votes
                })
            except Exception as e:
                print(f"Error extracting post: {e}")
        # Simulate scrolling down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new posts to load
        
        # Check if the number of posts increased
        new_post_count = len(posts_collected)
        if new_post_count == previous_post_count:
            print(f"No more new posts found after {scroll_attempts + 1} scrolls. Ending scroll.")
            break  # Stop if no new posts are found after scrolling
        
        previous_post_count = new_post_count  # Update the previous post count
        
        # Calculate new scroll height and compare it with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more content to load.")
            break  # Break the loop if the page height hasn't changed, meaning no new content
        last_height = new_height
        
        scroll_attempts += 1
        print(f"Scroll attempt {scroll_attempts}: Collected {len(posts_collected)} posts.")

    print(f"Total posts collected: {len(posts_collected)}")
    return posts_collected

# Main function to get posts based on parameters
def get_posts(source_type='frontpage', identifier=None, limit=2, sort='hot'):
    # Build URL based on source type (front page, subreddit, or user)
    if source_type == 'user':
        url = f"{BASE_URL}/user/{identifier}/posts/?sort={sort}"
    elif source_type == 'subreddit':
        url = f"{BASE_URL}/r/{identifier}/?sort={sort}"
    else:
        url = f"{BASE_URL}/?sort={sort}"

    driver = setup_driver()
    try:
        posts = fetch_posts(driver, url, limit)
    finally:
        driver.quit()  # Close the browser when done
    return posts

# Example usage
if __name__ == "__main__":
    # Parameters
    source_type = 'frontpage'  # Can be 'frontpage', 'user', or 'subreddit'
    identifier = 'technology'  # Subreddit name or username
    limit = 5                # Number of posts to retrieve
    sort = 'hot'               # Sorting option: 'hot', 'new', 'top', etc.

    posts = get_posts(source_type, identifier, limit, sort)
    for idx, post in enumerate(posts, 1):
        print(f"{idx}. Title: {post['title']}")
        print(f"   Votes: {post['votes']}")
        print(f"   Link: {post['link']}\n")
