from users import User

class Story:

    def __init__(self, name, rating, genre, category, synopsis, user, is_finished, chapter: list):
        self.name = name
        self.rating = rating
        self.genre = genre
        self.category = category
        self.synopsis = synopsis
        self.author: User = user
        self.is_finished: bool = is_finished
        self.chapters: list = chapter