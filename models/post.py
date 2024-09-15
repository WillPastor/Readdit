from scraper.comment_scraper import fetch_comments
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import setup_driver
import time
#from comment import Comment  # Import the Comment class
from models.comment_tree import CommentTree  # Import the CommentTree class



class Post:
    def __init__(self, baseurl, title, permalink, upvotes, downvotes, subreddit, user, time_posted, referring_url):
        self.base_url=baseurl
        self.title = title
        self.permalink = permalink
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.subreddit = subreddit
        self.user = user
        self.time_posted = time_posted
        self.referring_url = referring_url
        self.content = None
        self.comment_tree = CommentTree()  # Create a CommentTree instance for this post
        
    
    def get_content(self, base_url):
        # Fetches full content for the post (e.g., the full body of a post if it's a text post)
        full_url = f"{base_url}{self.permalink}"  # Using base_url
        driver = setup_driver()
        driver.get(full_url)

        try:
            # Wait for the content to be available
            wait = WebDriverWait(driver, 10)
            print("waiting for content element...")
            # Find the element containing the post content by class name
            content_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.text-neutral-content'))
            )

            # Extract the text from the <p> tags within this div
            paragraphs = content_element.find_elements(By.TAG_NAME, 'p')
            self.content = "\n".join([p.text for p in paragraphs])  # Join paragraphs with line breaks
        except Exception as e:
            print(f"Failed to load post content: {e}")
            self.content = None
        finally:
            driver.quit()
        return self.content

    

    def get_comments(self, base_url, full_url=None):
        # Fetch comments for the post
        if (full_url == None):
            full_url = f"{base_url}{self.permalink}"
        else:
            #override URL, gather comments from a provided link
            None
        driver = setup_driver()
        driver.get(full_url)

        try:
            # Wait for the comments to load
            wait = WebDriverWait(driver, 10)

            # Locate the comment elements by tag name 'shreddit-comment'
            comment_elements = wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'shreddit-comment'))
            )
            # Keep track of the most recent comment at each depth level
            parent_map = {0: None}  # Maps depth to the parent comment
            for comment_element in comment_elements:
                try:
                    # Extract comment attributes
                    comment_id = comment_element.get_attribute('thingid')
                    author = comment_element.get_attribute('author')

                    #text_element = comment_element.find_element(By.CSS_SELECTOR, f"div#t1_{comment_id}-comment-rtjson-content p")
                    #text = text_element.text


                    # Update the selector: using a more general approach to locate the comment text
                    try:
                        text_element = comment_element.find_element(By.CSS_SELECTOR, "div[slot='comment'] p")
                        text = text_element.text
                    except Exception as e:
                        print(f"Failed to extract text for comment {comment_id}: {e}")
                        text = "[Comment text not found]"

                    # Extract score and time
                    score_element = comment_element.find_element(By.CSS_SELECTOR, 'shreddit-comment-action-row')
                    score = score_element.get_attribute('score')
                    time_posted_element = comment_element.find_element(By.TAG_NAME, 'time')
                    time_posted = time_posted_element.get_attribute('datetime')

                    # Get the depth and parent_id (if applicable)
                    depth = int(comment_element.get_attribute('depth'))
                    #parent_id = comment_element.get_attribute('parentid') if depth > 0 else None
                    parent_id = parent_map.get(depth - 1)  # The parent is the most recent comment at depth - 1

                    # Add the comment to the CommentTree
                    self.comment_tree.add_comment(comment_id, author, text, score, time_posted, depth, parent_id)
                    
                    # Update the parent map
                    parent_map[depth] = comment_id  # This comment becomes the parent for the next depth level


                except Exception as e:
                    print(f"Failed to extract comment data: {e}")

        except Exception as e:
            print(f"Failed to load comments: {e}")
        finally:
            driver.quit()

        return self.comment_tree.get_root_comments()

