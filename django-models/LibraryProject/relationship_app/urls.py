from django.shortcuts import render
from .models import Book

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()  # ✅ This is the required query
    return render(request, 'list_books.html', {'books': books})
