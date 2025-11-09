import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")  # adjust if your settings module name differs
django.setup()

from .models import Author, Library

def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        return author.book_set.all()
    except Author.DoesNotExist:
        return []

def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []

def librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        # Access related Librarian via OneToOne: library.librarian
        return library.librarian
    except Library.DoesNotExist:
        return None
    except Exception:
        return None

if __name__ == "__main__":
    print("Books by 'Jane Austen':", list(books_by_author('Jane Austen')))
    print("Books in 'Central Library':", list(books_in_library('Central Library')))
    print("Librarian for 'Central Library':", librarian_for_library('Central Library'))
