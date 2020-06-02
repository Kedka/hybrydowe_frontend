class Book:
    def __init__(self, id, title, author, booked):
        self.id = id
        self.title = title
        self.author = author
        self.booked = booked


class Author:
    def __init__(self, id, name, surname):
        self.id = id
        self.name = name
        self.surname = surname

    def __str__(self):
        return self.name + self.surname
