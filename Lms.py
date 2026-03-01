import json
import datetime
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, book_id, available, borrow_date = None, due_date = None):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.available = available
        self.borrow_date = borrow_date
        self.due_date = due_date
        pass
    def display_info(self):
        status = "Available" if self.available else f"Borrowed (Due: {self.due_date})"
        print(f"{self.title} by {self.author} | ID: {self.book_id} | Status: {status}")
        if not self.available:
            print(f"  Borrowed on: {self.borrow_date}")
            print(f"  Due date: {self.due_date}")
    def mark_borrowed(self):
        self.available = False
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=7)
        self.borrow_date = self.borrow_date.strftime("%Y-%m-%d")
        self.due_date = self.due_date.strftime("%Y-%m-%d")
    def mark_returned(self):
        self.available = True
        self.borrow_date = None
        self.due_date = None


#user class

class User:
    def __init__(self, name, user_id, borrowed_books=None):
        self.name = name
        self.user_id = user_id
        # self.borrowed_books = borrowed_books
        if borrowed_books is None:
            self.borrowed_books = []
        else:
            self.borrowed_books = borrowed_books
    def borrow_book(self, book):
        if len(self.borrowed_books) >= 3:
            print("You cannot borrow more than 3 books.")
            return False
        if not book.available:
            print("This book is not available.")
            return False
        
        self.borrowed_books.append(book.book_id)
        book.mark_borrowed()
        print("Book borrowed successfully.")
        return True
    def return_book(self, book):
        if book.book_id not in self.borrowed_books:
            print("You did not borrow this book.")
            return False
        
        self.borrowed_books.remove(book.book_id)
        book.mark_returned()
        print("Book returned successfully.")
        return True
    def display_info(self):
        print(f"User: {self.name} | ID: {self.user_id}")
        if self.borrowed_books:
            print("Borrowed Books:")
            for book_id in self.borrowed_books:
                print(f"  - Book ID: {book_id}")
        else:
            print("No books currently borrowed.")

#libarary class


class Library:
    def __init__(self):
        self.list_of_books = []
        self.list_of_users = []
        self.load_data()

    def add_book(self, title, author, book_id):
        for book in self.list_of_books:
            if book.book_id == book_id:
                print("Book ID already exists.")
                return
        self.list_of_books.append(Book(title, author, book_id, available=True))
        print("Book added successfully.")
    def remove_book(self, book_id):
        for book in self.list_of_books:
            if book.book_id == book_id:
                self.list_of_books.remove(book)
                print("Book removed successfully.")
                return
        print("Book not found.")
    def search_book_by_title(self, title):
        found = False
        for book in self.list_of_books:
            if title.lower() in book.title.lower():
                book.display_info()
                found = True
        if not found:
            print("Book not found.")
    def show_all_books(self):
        if not self.list_of_books:
            print("No books available.")
            return
        for book in self.list_of_books:
            book.display_info()

    def register_user(self, name, user_id):
        for user in self.list_of_users:
            if user.user_id == user_id:
                print("User ID already exists.")
                return
        self.list_of_users.append(User(name, user_id))
        print("User registered successfully.")
    def lend_book(self, user_id, book_id):
        user = self.get_user(user_id)
        book = self.get_book(book_id)
        if user and book:
            if user.borrow_book(book):
                print("Book lent successfully.")
            else:
                print("Failed to lend book.")
    def return_book(self, user_id, book_id):
        user = self.get_user(user_id)
        book = self.get_book(book_id)
        if user and book:
            if user.return_book(book):
                print("Book returned successfully.")
            else:
                print("Failed to return book.")
    def get_user(self, user_id):
        for user in self.list_of_users:
            if user.user_id == user_id:
                return user
        print("User not found.")
        return None
    def get_book(self, book_id):
        for book in self.list_of_books:
            if book.book_id == book_id:
                return book
        print("Book not found.")
        return None
    def save_data(self):
        data = {
            "books": [
                {
                    "title": book.title,
                    "author": book.author,
                    "book_id": book.book_id,
                    "available": book.available,
                    "borrow_date": book.borrow_date,
                    "due_date": book.due_date
                } for book in self.list_of_books
            ],
            "users": [
                {
                    "name": user.name,
                    "user_id": user.user_id,
                    "borrowed_books": user.borrowed_books
                } for user in self.list_of_users
            ]
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")
    def load_data(self):
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)
                self.list_of_books = [Book(**book) for book in data.get("books", [])]
                self.list_of_users = [User(**user) for user in data.get("users", [])]
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No existing data found. Starting with an empty library.")



def main():
    library = Library()
    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book by Title")
        print("4. Show All Books")
        print("5. Register User")
        print("6. Lend Book")
        print("7. Return Book")
        print("8. Save & Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            book_id = input("Enter book ID: ")
            library.add_book(title, author, book_id)
        elif choice == "2":
            book_id = input("Enter book ID to remove: ")
            library.remove_book(book_id)
        elif choice == "3":
            title = input("Enter book title to search: ")
            library.search_book_by_title(title)
        elif choice == "4":
            library.show_all_books()
        elif choice == "5":
            name = input("Enter user name: ")
            user_id = input("Enter user ID: ")
            library.register_user(name, user_id)
        elif choice == "6":
            user_id = input("Enter user ID: ")
            book_id = input("Enter book ID to lend: ")
            library.lend_book(user_id, book_id)
        elif choice == "7":
            user_id = input("Enter user ID: ")
            book_id = input("Enter book ID to return: ")
            library.return_book(user_id, book_id)
        elif choice == "8":
            library.save_data()
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()