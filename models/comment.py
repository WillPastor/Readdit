class Comment:
    def __init__(author, text, score, time_posted, depth=0, parent=None):
        self.author = author
        self.text = text
        self.score = score
        self.time_posted = time_posted
        self.parent = parent  # Reference to the parent comment (None if it's a top-level comment)
        self.children = []    # List of replies (child comments)
        self.depth = depth    # Depth in the comment tree (0 for top-level comments)
    def __repr__(self):
            return f"Comment by {self.author}: {self.text} (Score: {self.score}, Posted: {self.time_posted})"
