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
    posts = fetch_posts(subreddit=subreddit, base_url=base_url, limit=1, sort='hot')

    #for post in posts:
        #print(f"Post Title: {post.title}")
        #print(f"Post Upvotes: {post.upvotes}")
        #print(f"Post Link: {post.permalink}")

        # Load post content (if needed)
        #content = post.get_content(base_url=base_url)#(baseurl=base_url)
        
        #print(f"Post Content: {content}")
    
    
    # Fetch and print comments
    #root_comments = posts[0].get_comments(base_url=base_url)
    #for comment in root_comments:
    #    print("root comment: " + str(comment))  # Top-level comments
    #    for child in comment.children:
    #        print(f"  Reply: {child}")  # Replies to top-level comments
    
    #for post in posts:
    #        print(f"Post Title: {post.title}")
    #        print(f"Post Upvotes: {post.upvotes}")
    #        print(f"Post Link: {post.permalink}")
    #        root_comments = post.get_comments(base_url=base_url)
    #        for comment in root_comments:
    #            print(f"Root comment: {comment}")  # Prints the comment using __str__
    #            for child in comment.children:
    #                print(f"  Reply: {child}")  # Prints the replies (child comments)
    print("\nPrinting posts: \n")
    for post in posts:
        print(f"Post Title: {post.title}")
        print(f"Post Upvotes: {post.upvotes}")
        print(f"Post Link: {post.permalink}")
        content = post.get_content(base_url=base_url)
        print(f"Post Content: {content}")
        # Fetch and print comments with a depth limit
        root_comments = post.get_comments(base_url=base_url)
        #print("\nTraversing comments with no depth limit:")
        #post.comment_tree.traverse()  # Traverse without depth limit

        print("\nTraversing comments with depth limit 4:")
        post.comment_tree.traverse(depth_limit=4)  # Traverse with depth limit 1