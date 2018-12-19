# Book class has seven attributes to hold the data that a book in the book table stores

class Products:

    def __init__(self, id, title, author, edition, price, isbn, units):
        self.id = id
        self.title = title
        self.author = author
        self.edition = edition
        self.price = price
        self.isbn = isbn
        self.units = units