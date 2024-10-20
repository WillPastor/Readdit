from scraper.post_scraper import fetch_posts, fetch_post_content
from scraper.comment_scraper import fetch_comments

def main():
    base_url = "https://reddit.com"
    subreddit = 'AmIOverreacting'

    # Fetch posts from a subreddit
    posts = fetch_posts(subreddit=subreddit, base_url=base_url, limit=3, sort='hot')

    # Fetch and set post content and comments
    for post in posts:
        # Fetch and set post content
        content = fetch_post_content(post)
        post.set_content(content)

        # Fetch and set comments
        comment_tree = fetch_comments(post.permalink, base_url)
        post.set_comments(comment_tree)

        # Print post details
        print(f"\nPost Title: {post.title}")
        print(f"Post Upvotes: {post.upvotes}")
        print(f"Post Link: {post.permalink}")
        print(f"Post Content: {post.content}")

        # Traverse and print comments with a depth limit
        print("\nTraversing comments with depth limit 4:")
        post.comment_tree.traverse(depth_limit=4)

if __name__ == "__main__":
    main()
