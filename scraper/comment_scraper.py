from models.comment import Comment
from utils import setup_driver
from selenium.webdriver.common.by import By
import time

def fetch_comments(post_url, base_url, sort='top'):
    sorted_comments_url = f"{base_url}{post_url}?sort={sort}"
    driver = setup_driver()
    driver.get(sorted_comments_url)
    time.sleep(3)

    comments = []
    try:
        comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div.comment-container')
        for comment_element in comment_elements:
            content = comment_element.find_element(By.CSS_SELECTOR, 'div.comment-content').text.strip()
            upvotes = comment_element.find_element(By.CSS_SELECTOR, 'span.comment-upvotes').text.strip()
            downvotes = comment_element.find_element(By.CSS_SELECTOR, 'span.comment-downvotes').text.strip()
            user = comment_element.find_element(By.CSS_SELECTOR, 'a.comment-user').text.strip()
            time_posted = comment_element.find_element(By.CSS_SELECTOR, 'time.comment-time').get_attribute('datetime')

            comment = Comment(content, upvotes, downvotes, user, time_posted)
            comments.append(comment)
    except Exception as e:
        print(f"Error loading comments: {e}")
    finally:
        driver.quit()

    return comments