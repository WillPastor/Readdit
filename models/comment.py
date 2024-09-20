class Comment:
    def __init__(self, author, text, score, time_posted, depth=0, parent_id=None, parent_comment=None):
        self.author = author
        self.text = text
        self.score = score
        self.time_posted = time_posted
        self.depth = depth    # Depth level in the comment tree
        self.parent_id = parent_id  
        self.parent_comment = parent_comment
        self.children = []    # List of replies (child comments)
        
    
    def add_child(self, child_comment):
        """Add a child (reply) to this comment."""
        self.children.append(child_comment)
    
    def __str__(self):
            return f"Comment by {self.author} (Depth {self.depth}): {self.text} (Score: {self.score}, Posted: {self.time_posted})"

    def __repr__(self):
        return self.__str__()  # For debugging, return the same as __str__

    #def get_parent(self):
        # Reference to the parent comment (None if it's a top-level comment)