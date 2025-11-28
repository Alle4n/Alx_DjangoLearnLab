# Book API Views (Django REST Framework)

This module implements full CRUD operations for the Book model using DRF generic class-based views.

## Views Included
- BookListView – GET all books
- BookDetailView – GET one book
- BookCreateView – POST new book (authenticated only)
- BookUpdateView – PUT/PATCH update a book (authenticated only)
- BookDeleteView – DELETE a book (authenticated only)

## Permissions
- Read operations: public access
- Write operations: restricted to authenticated users

## URL Structure
/books/                     → List
/books/<pk>/                → Detail
/books/create/              → Create
/books/<pk>/update/         → Update
/books/<pk>/delete/         → Delete
