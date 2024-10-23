# Readdit

**Readdit** is an ongoing Reddit scraping project designed to collect posts and comments from Reddit for training machine learning and AI models. The goal of Readdit is to efficiently gather data, including post content and comments, in a structured way. This data can be used for future analysis and machine learning training purposes.

## Features

- **Scraping Reddit Posts:** Scrapes posts from specific subreddits based on sorting criteria (e.g., hot, new, top).
- **Scraping Reddit Comments:** Gathers comments from posts and builds a comment tree with depth control for easier analysis.
- **Customizable Scraper Settings:** Configurable options such as scrolling attempts, wait times, and data limits to adapt the scraping to your needs.

## Project Structure

- **`main.py`**: The entry point of the application. This script configures the scraping process, including selecting the subreddit and fetching posts and comments.
- **`post_scraper.py`**: Handles the scraping of Reddit posts using Selenium. It simulates scrolling to load more content and extracts the post details.
- **`comment_scraper.py`**: Scrapes comments from Reddit posts. It constructs a `CommentTree` for better organization and traversal of the comment hierarchy.
- **`post.py`**: Defines the `Post` class, which represents a Reddit post and contains methods for setting the content and comments.
- **`comment.py`**: Defines the `Comment` class, which represents a comment with attributes such as author, text, score, and depth.
- **`comment_tree.py`**: Manages the structure of comments as a tree, allowing for easy traversal of replies and nested comments.
- **`utils.py`**: Contains utility functions for setting up the Selenium driver and other helper methods.
- **`page_identifiers.py`**: Specifies the CSS selectors and attribute names used to identify elements on Reddit pages during scraping.
- **`scraper_settings.py`**: Configurable settings for the scraper, such as base URL, default post limit, maximum scroll attempts, and wait times.

## Requirements

- **Python 3.7+**
- **Selenium** for browser automation.
- **BeautifulSoup4** for parsing expanded comment data.
- **webdriver-manager** for automatically managing the ChromeDriver.

## Installation

1. Clone the repository: `git clone https://github.com/WillPastor/Readdit.git`

   Install the required packages using the following command:

## Usage

1. Update the settings in `scraper_settings.py` to customize scraping behavior if needed.

2. First, install the requirements: `pip install -r requirements.txt`

3. Run the scraper: `.\main.py`

   &#x20;

## Configuration

The settings can be adjusted in `scraper_settings.py`:

- **`base_url`**: Base URL of Reddit.
- **`default_limit`**: Number of posts to scrape per run.
- **`max_scroll_attempts`**: Number of scrolling attempts for more posts.
- **`scroll_wait_time`**: Time to wait between scrolls for posts to load.

## Limitations

- The scraper uses Selenium to simulate a user browsing Reddit, which is subject to rate limiting and IP blocking. Use responsibly.
- Expanding deeply nested comments may require additional network requests and can be rate-limited by Reddit. Currently, the scraper cannot reliably fetch nested comments beyond a certain depth.

## License

This project is licensed under the MIT License.

## Contributions

Contributions are welcome! Feel free to open an issue or create a pull request.

## Future Improvements

- **Data Storage**: Store scraped data in a database for easier access and analysis.
- **Error Handling**: Improve error handling during scraping, especially around loading failures and rate limits.
- **Enhanced Data Analysis**: Add features for analyzing and processing the collected data, such as sentiment analysis, filtering, and searching.
- **Content Navigation**: Implement a feature to follow content references (e.g., "in my previous post" or "read u/\_\_\_'s post about \_\_\_") and maintain a traceable history of navigated content (content trail).
- **Alternative Scraping Methods and API Integration**: Add an option to use Reddit's official API or other scraping methods as alternatives. Using Reddit's official API can reduce the likelihood of IP blocking and improve the reliability of the data collected.

## Contact

For questions or suggestions, please reach out to me at [wipastor@ursinus.edu](mailto\:wipastor@ursinus.edu).
