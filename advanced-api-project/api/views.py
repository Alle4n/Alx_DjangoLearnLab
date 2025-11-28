from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# ListView: Retrieves all books (GET /books/)
# Anyone can view (Read-only for unauthenticated users).
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access


# DetailView: Retrieve a single book by ID (GET /books/<pk>/)
# Read-only for unauthenticated users.
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# CreateView: Add a new book (POST /books/create/)
# Only authenticated users can create.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    # Override perform_create to customize save behavior
    def perform_create(self, serializer):
        # Custom logic can be added here (logging, validation hooks, etc.)
        serializer.save()


# UpdateView: Modify existing book (PUT/PATCH /books/<pk>/update/)
# Only authenticated users can update.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Customize update logic
    def perform_update(self, serializer):
        # Custom validation or hooks can be added
        serializer.save()


# DeleteView: Remove a book (DELETE /books/<pk>/delete/)
# Only authenticated users can delete.
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
