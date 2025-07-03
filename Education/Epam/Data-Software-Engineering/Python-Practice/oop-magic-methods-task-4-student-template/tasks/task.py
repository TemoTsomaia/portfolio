class PriceControl:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("Price must be between 0 and 100.")
        setattr(instance, self.private_name, value)


class NameControl:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        if hasattr(instance, self.private_name):
            public_name = self.private_name[1:]
            raise ValueError(f"{public_name.capitalize()} can not be changed.")
        setattr(instance, self.private_name, value)






class Book:
    author = NameControl()
    name = NameControl()
    price = PriceControl()

    def __init__(self, author, name, price):
        self.author = author
        self.name = name
        self.price = price

    def __str__(self):
        return f"Author: {self.author}, Name: {self.name}, Price: {self.price}"

    def __repr__(self):
        return f"Book(Author={self.author}, Name={self.name}, Price={self.price})"


