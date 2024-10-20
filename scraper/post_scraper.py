from models.post import Post
from utils import setup_driver, scroll_to_bottom
from config.page_identifiers import IDENTIFIERS
from config.scraper_settings import CONFIG
from selenium.webdriver.common.by import By
import time

def fetch_posts(subreddit, base_url=CONFIG['base_url'], limit=CONFIG['default_limit'], max_scroll_attempts=CONFIG['max_scroll_attempts'], sort='hot'):
    """
    Fetches posts from a subreddit using Selenium with simulated scrolling.
    Args:
    - subreddit: the name of the subreddit to fetch posts from.
    - base_url: the base URL of the site (e.g., https://reddit.com).
    - limit: the maximum number of posts to collect.
    - max_scroll_attempts: the number of times to scroll down to fetch more posts.
    - sort: sorting option for the posts (hot, new, top).

    Returns:
    - A list of Post objects.
    """
    full_url = f"{base_url}/r/{subreddit}/?sort={sort}"
    driver = setup_driver()
    driver.get(full_url)
    time.sleep(CONFIG['scroll_wait_time'])  # Wait for the page to load
    posts_collected = []
    
    previous_post_count = 0
    scroll_attempts = 0

    while len(posts_collected) < limit and scroll_attempts < max_scroll_attempts:
        # DEBUG: Print current page URL
        print(f"Current page URL: {driver.current_url}")
        
        # Find articles that represent each post
        articles = driver.find_elements(By.CSS_SELECTOR, IDENTIFIERS['post_article'])
        
        print(f"Found {len(articles)} articles on this scroll.")

        for article in articles:
            if len(posts_collected) >= limit:
                break
            try:
                shreddit_post = article.find_element(By.CSS_SELECTOR, IDENTIFIERS['shreddit_post'])
                # Extract post attributes
                title = shreddit_post.get_attribute(IDENTIFIERS['post_title'])
                permalink = shreddit_post.get_attribute(IDENTIFIERS['post_permalink'])
                votes = shreddit_post.get_attribute(IDENTIFIERS['post_votes'])
                subreddit_name = article.get_attribute(IDENTIFIERS['post_subreddit_name'])
                author = shreddit_post.get_attribute(IDENTIFIERS['post_author'])
                time_posted = shreddit_post.get_attribute(IDENTIFIERS['post_timestamp'])

                # Create a Post object and append it to the list
                post = Post(
                    base_url=base_url,
                    title=title,
                    permalink=permalink,
                    upvotes=votes,
                    downvotes=None,
                    subreddit=subreddit_name,
                    user=author,
                    time_posted=time_posted,
                    referring_url=full_url
                )
                posts_collected.append(post)
            except Exception as e:
                print(f"Error extracting post: {e}")
        
        # Simulate scrolling down
        scroll_to_bottom(driver)
        time.sleep(CONFIG['scroll_wait_time'])  # Wait for new posts to load
        
        # Check if the number of posts increased
        new_post_count = len(posts_collected)
        if new_post_count == previous_post_count:
            print(f"No more new posts found after {scroll_attempts + 1} scrolls. Ending scroll.")
            break  # Stop if no new posts are found after scrolling
        
        previous_post_count = new_post_count  # Update the previous post count
        
        scroll_attempts += 1
        print(f"Scroll attempt {scroll_attempts}: Collected {len(posts_collected)} posts.")

    print(f"Total posts collected: {len(posts_collected)}")
    driver.quit()
    return posts_collected


def fetch_post_content(post):
    """Fetches the full content of a post."""
    full_url = f"{post.base_url}{post.permalink}"
    driver = setup_driver()
    driver.get(full_url)

    try:
        content_element = driver.find_element(By.CSS_SELECTOR, IDENTIFIERS['post_content'])
        paragraphs = content_element.find_elements(By.TAG_NAME, IDENTIFIERS['post_paragraph'])
        post.content = "\n".join([p.text for p in paragraphs])
    except Exception as e:
        print(f"Failed to load post content: {e}")
        post.content = None
    finally:
        driver.quit()

    return post.content