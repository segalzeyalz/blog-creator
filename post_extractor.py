class PostExtractor:
    @staticmethod
    def extract(blog_post: dict):
        likes_and_dislike = blog_post.get("likes", {})
        only_likes = [username for username, is_liked in likes_and_dislike.items() if is_liked is True]
        return {
            "postId": blog_post.get("postId"),
            "title": blog_post.get("title"),
            "text": blog_post.get("text"),
            "author": blog_post.get("author"),
            "likesAmount": len(only_likes)
        }