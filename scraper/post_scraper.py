from models.post import Post
from utils import setup_driver
from selenium.webdriver.common.by import By
import time

def fetch_posts(subreddit, base_url, limit=10, max_scroll_attempts=2, sort='hot'):
    """
    Fetches posts from a subreddit using Selenium with simulated scrolling.
    Args:
    - subreddit: the name of the subreddit to fetch posts from.
    - base_url: the base URL of the site (e.g., https://reddit-like-site.com).
    - limit: the maximum number of posts to collect.
    - max_scroll_attempts: the number of times to scroll down to fetch more posts.
    - sort: sorting option for the posts (hot, new, top).

    Returns:
    - A list of Post objects.
    """
    full_url = f"{base_url}/r/{subreddit}/?sort={sort}"
    driver = setup_driver()
    driver.get(full_url)
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
                shreddit_post = article.find_element(By.CSS_SELECTOR, 'shreddit-post')
                # Find the title of the post
                #title = article.get_attribute('aria-label')  # Extract the aria-label attribute which holds the title
                title= shreddit_post.get_attribute('post-title')
                print(f"Post Title: {title}")
                
                # Get the permalink for the post
                #permalink = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                permalink = shreddit_post.get_attribute('permalink')
                print(f"Post Permalink: {permalink}")

                # Extract the votes if available
                votes = shreddit_post.get_attribute('score')
                
                # Extract subreddit, author, and post time (adjust based on actual structure)
                subreddit_name = article.get_attribute('subreddit-prefixed-name')
                author = shreddit_post.get_attribute('author')
                time_posted = shreddit_post.get_attribute('created-timestame') #article.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')

                # Create a Post object and append it to the list
                post = Post(
                    baseurl=base_url,
                    title=title,
                    permalink=permalink,
                    upvotes=votes,  # Assuming no separate downvotes available
                    downvotes=None,  # Optional: handle if available
                    subreddit=subreddit_name,
                    user=author,
                    time_posted=time_posted,
                    referring_url=full_url
                )
                posts_collected.append(post)
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
    driver.quit()
    return posts_collected