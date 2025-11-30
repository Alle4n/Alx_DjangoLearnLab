from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django_filters import rest_framework as filters        # ✔ required
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Book
from .serializers import BookSerializer


# READ: Anyone
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filtering, searching, ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,        # ✔ required string
        filters.OrderingFilter,      # ✔ required string
    ]

    filterset_fields = ['title', 'author', 'category']
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['title']


# READ: Anyone
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# CREATE: Authenticated only
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# UPDATE: Authenticated only
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


# DELETE: Authenticated only
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
