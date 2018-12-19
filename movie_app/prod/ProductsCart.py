# BookInCart class has six attributes to hold the data that a book in the cart table stores

class ProductsCart:

    def __init__(self, id, part, price, partNum, quantity, total):
        self.id = id
        self.part = part
        self.price = price
        self.partNum = partNum
        self.quantity = quantity
        self.total = total