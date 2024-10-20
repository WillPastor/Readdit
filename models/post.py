class Post:
    def __init__(self, base_url, title, permalink, upvotes, downvotes, subreddit, user, time_posted, referring_url):
        self.base_url = base_url
        self.title = title
        self.permalink = permalink
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.subreddit = subreddit
        self.user = user
        self.time_posted = time_posted
        self.referring_url = referring_url
        self.content = None
        self.comment_tree = None

    def set_content(self, content):
        self.content = content

    def set_comments(self, comment_tree):
        self.comment_tree = comment_tree
