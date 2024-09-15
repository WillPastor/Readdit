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

from scraper.post_scraper import fetch_posts

if __name__ == "__main__":
    # Define the base URL
    base_url = "https://reddit.com"

    # Fetch posts from a subreddit
    subreddit = 'AmIOverreacting'
    posts = fetch_posts(subreddit=subreddit, base_url=base_url, limit=1, sort='new')

    for post in posts:
        print(f"Post Title: {post.title}")
        print(f"Post Upvotes: {post.upvotes}")
        print(f"Post Link: {post.permalink}")

        # Load post content (if needed)
        content = post.get_content(base_url=base_url)#(baseurl=base_url)
        print(f"Post Content: {content}")

    
    # Fetch and print comments
    #root_comments = posts[0].get_comments(base_url=base_url)
    #for comment in root_comments:
        #print(comment)  # Top-level comments
        #for child in comment.children:
            #print(f"  Reply: {child}")  # Replies to top-level comments
