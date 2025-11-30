from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


# READ: Anyone
# Includes: filtering, searching, ordering
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filter/search/order
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering by fields
    filterset_fields = ['title', 'author', 'publication_year']
