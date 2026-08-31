from enum import Enum
from abc import ABC, abstractmethod


class ItemStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"


class LibraryItem(ABC):
    """Base class for all library items."""

    def __init__(self, title):
        self.title = title
        self.__status = ItemStatus.AVAILABLE

    @property
    def status(self):
        return self.__status

    def checkout(self):
        if self.__status == ItemStatus.AVAILABLE:
            self.__status = ItemStatus.CHECKED_OUT
            return True
        return False

    def return_item(self):
        if self.__status == ItemStatus.CHECKED_OUT:
            self.__status = ItemStatus.AVAILABLE
            return True
        return False

    def mark_lost(self):
        if self.__status != ItemStatus.LOST:
            self.__status = ItemStatus.LOST
            return True
        return False

    @property
    @abstractmethod
    def loan_period(self):
        """Each subclass must define its own loan period (in days)."""
        pass

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __str__(self):
        return f"{self.title} ({self.__class__.__name__}) - {self.status.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self.title}')"

    @staticmethod
    def is_valid_isbn(isbn):
        """Validates an ISBN-13 checksum."""
        isbn = isbn.replace("-", "").replace(" ", "")

        if len(isbn) != 13 or not isbn.isdigit():
            return False

        total = 0
        for i in range(12):
            if i % 2 == 0:
                total += int(isbn[i])
            else:
                total += int(isbn[i]) * 3

        check = (10 - (total % 10)) % 10
        return check == int(isbn[12])

    @classmethod
    def from_dict(cls, data):
        """Builds the right item from a dict, then applies its saved status."""
        item = cls.build(data)

        status = data.get("status", ItemStatus.AVAILABLE.value)
        if status == ItemStatus.CHECKED_OUT.value:
            item.checkout()
        elif status == ItemStatus.LOST.value:
            item.mark_lost()

        return item

    @classmethod
    def build(cls, data):
        """Each subclass creates itself from a dict here."""
        raise NotImplementedError

    def to_dict(self):
        return {"type": self.__class__.__name__, "title": self.title,
                "status": self.status.value}


class Book(LibraryItem):
    loan_period = 21

    def __init__(self, title, author, isbn):
        super().__init__(title)
        self.author = author
        self.isbn = isbn

    @classmethod
    def build(cls, data):
        return cls(data["title"], data["author"], data["isbn"])

    def to_dict(self):
        d = super().to_dict()
        d["author"] = self.author
        d["isbn"] = self.isbn
        return d


class DVD(LibraryItem):
    loan_period = 5

    def __init__(self, title, director):
        super().__init__(title)
        self.director = director

    @classmethod
    def build(cls, data):
        return cls(data["title"], data["director"])

    def to_dict(self):
        d = super().to_dict()
        d["director"] = self.director
        return d


class Magazine(LibraryItem):
    loan_period = 14

    def __init__(self, title, issue):
        super().__init__(title)
        self.issue = issue

    @classmethod
    def build(cls, data):
        return cls(data["title"], data["issue"])

    def to_dict(self):
        d = super().to_dict()
        d["issue"] = self.issue
        return d



item_types = {
    "Book": Book,
    "DVD": DVD,
    "Magazine": Magazine,
}


class Library:


    def __init__(self, database=None):
        self.items = []
        self.database = database

    def add_item(self, item):
        self.items.append(item)

    def checkout(self, title):
        item = self.find_by_title(title)
        if item:
            return item.checkout()
        return False

    def return_item(self, title):
        item = self.find_by_title(title)
        if item:
            return item.return_item()
        return False

    def find_by_title(self, title):
        for item in self.items:
            if item.title.lower() == title.lower():
                return item
        return None

    def list_available(self):
        for item in sorted(self.items):
            if item.status == ItemStatus.AVAILABLE:
                print(item)

    def list_all(self):
        for item in sorted(self.items):
            print(item)

    def save(self):
        if self.database:
            self.database.save(self.items)

    def load(self):
        if self.database:
            self.items = self.database.load()


class Database:


    _instance = None

    def __new__(cls, filename="database.txt"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filename="database.txt"):
        if self._initialized:
            return
        self.filename = filename
        self._initialized = True

    def save(self, items):
        with open(self.filename, "w") as file:
            for item in items:
                fields = item.to_dict()
                line = "|".join(f"{key}={value}" for key, value in fields.items())
                file.write(line + "\n")

    def load(self):
        items = []
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    data = {}
                    for part in line.split("|"):
                        key, value = part.split("=", 1)
                        data[key] = value

                    item_class = item_types[data["type"]]
                    items.append(item_class.from_dict(data))
        except FileNotFoundError:
            return []

        return items




def add_item_menu(library):
    print("1) Book  2) DVD  3) Magazine")
    choice = input("Item type: ").strip()

    title = input("Title: ").strip()

    if choice == "1":
        author = input("Author: ").strip()
        isbn = input("ISBN-13: ").strip()
        if not LibraryItem.is_valid_isbn(isbn):
            print("Warning: this ISBN is not valid, item added anyway.")
        library.add_item(Book(title, author, isbn))

    elif choice == "2":
        director = input("Director: ").strip()
        library.add_item(DVD(title, director))

    elif choice == "3":
        issue = input("Issue: ").strip()
        library.add_item(Magazine(title, issue))

    else:
        print("Invalid choice.")
        return

    print("Item added.")


def menu():
    db = Database("database.txt")
    library = Library(database=db)
    library.load()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add item")
        print("2. Checkout item")
        print("3. Return item")
        print("4. Show available items")
        print("5. Show all items")
        print("6. Save to file")
        print("7. Check ISBN validity")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_item_menu(library)

        elif choice == "2":
            title = input("Title to checkout: ").strip()
            print("Success!" if library.checkout(title) else "Could not checkout item.")

        elif choice == "3":
            title = input("Title to return: ").strip()
            print("Success!" if library.return_item(title) else "Could not return item.")

        elif choice == "4":
            library.list_available()

        elif choice == "5":
            library.list_all()

        elif choice == "6":
            library.save()
            print("Saved to", db.filename)

        elif choice == "7":
            isbn = input("Enter ISBN-13: ").strip()
            print("Valid!" if LibraryItem.is_valid_isbn(isbn) else "Not valid.")

        elif choice == "0":
            print("Bye!")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()