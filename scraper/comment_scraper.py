from models.comment_tree import CommentTree
from utils import setup_driver, scroll_to_bottom
from config.page_identifiers import IDENTIFIERS
from config.scraper_settings import CONFIG
from selenium.webdriver.common.by import By
import time

def fetch_comments(post_url, base_url=CONFIG['base_url'], sort='top'):
    sorted_comments_url = f"{base_url}{post_url}?sort={sort}"
    driver = setup_driver()
    driver.get(sorted_comments_url)
    time.sleep(CONFIG['scroll_wait_time'])

    comment_tree = CommentTree()
    parent_map = {0: None}  # Maps depth to the parent comment

    try:
        comment_elements = driver.find_elements(By.CSS_SELECTOR, IDENTIFIERS['comment_element'])
        for comment_element in comment_elements:
            try:
                # Extract comment attributes
                comment_id = comment_element.get_attribute(IDENTIFIERS['comment_id'])
                author = comment_element.get_attribute(IDENTIFIERS['comment_author'])
                text_element = comment_element.find_element(By.CSS_SELECTOR, IDENTIFIERS['comment_text'])
                text = text_element.text if text_element else "[Comment text not found]"
                score_element = comment_element.find_element(By.CSS_SELECTOR, IDENTIFIERS['comment_score'])
                score = score_element.get_attribute(IDENTIFIERS['comment_score_value'])
                time_posted_element = comment_element.find_element(By.TAG_NAME, IDENTIFIERS['comment_time'])
                time_posted = time_posted_element.get_attribute('datetime')
                depth = int(comment_element.get_attribute(IDENTIFIERS['comment_depth']))
                parent_id = parent_map.get(depth - 1)

                # Add comment to CommentTree
                comment_tree.add_comment(comment_id, author, text, score, time_posted, depth, parent_id)
                parent_map[depth] = comment_id
            except Exception as e:
                print(f"Failed to extract comment data: {e}")
    except Exception as e:
        print(f"Failed to load comments: {e}")
    finally:
        driver.quit()

    return comment_tree