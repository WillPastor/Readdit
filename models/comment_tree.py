# comment_tree.py

from models.comment import Comment

class CommentTree:
    def __init__(self):
        self.root_comments = []  # List of top-level comments
        self.all_comments = {}   # Dictionary mapping comment IDs to Comment objects

    def add_comment(self, comment_id, author, text, score, time_posted, depth, parent_id=None):
        """
        Adds a comment to the tree. If it has a parent, it will be added as a child of the parent.
        """
        parent_comment = self.all_comments.get(parent_id) if parent_id else None
        comment = Comment(author=author, text=text, score=score, time_posted=time_posted, depth=depth, parent_id=parent_id, parent_comment=parent_comment)

        # Store the comment in the tree
        self.all_comments[comment_id] = comment

        # If it's a top-level comment, add it to the root_comments list
        if parent_comment is None:
            self.root_comments.append(comment)
        else:
            # If it's a reply, add it to the parent's children
            parent_comment.add_child(comment)

    
    def traverse(self, depth_limit=None):
        """Traverse the entire comment tree starting from root comments."""
        traversal_results=[]
        for comment in self.root_comments:
            self._traverse_comment(comment, current_depth=0, depth_limit=depth_limit, traversal_results=traversal_results)
        return traversal_results

    def _traverse_comment(self, comment, current_depth, depth_limit, traversal_results=[]):
        """
        A helper function to recursively traverse the comment tree.
        Prints each comment and its children recursively.
        :param comment: The current comment being traversed.
        :param current_depth: The current depth level.
        :param depth_limit: Maximum depth to traverse. If None, no limit is applied.
        """
        # Print the current comment
        print("  " * current_depth + f"Comment by {comment.author} (Score: {comment.score}, Depth: {comment.depth}): {comment.text}")
        traversal_results.append(comment)
        # If depth limit is reached, stop further traversal
        if depth_limit is not None and current_depth >= depth_limit:
            return

        # Recursively traverse children
        for child in comment.children:
            self._traverse_comment(child, current_depth + 1, depth_limit)


    def get_root_comments(self):
        """Return the list of top-level comments."""
        return self.root_comments

    def get_all_comments(self):
        """Return a dictionary of all comments in the tree."""
        return self.all_comments

    def get_comment_by_id(self, comment_id):
        """Retrieve a comment by its ID."""
        return self.all_comments.get(comment_id)

    def __repr__(self):
        return f"CommentTree with {len(self.all_comments)} comments"
