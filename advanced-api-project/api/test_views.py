from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        """Prepare test data and test users."""
        self.client = APIClient()

        # Create a user for authenticated actions
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Create Author
        self.author = Author.objects.create(name="John Doe")

        # Create sample books
        self.book1 = Book.objects.create(
            title="Book One",
            publication_year=2001,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Another Book",
            publication_year=2020,
            author=self.author
        )

        # URLs
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        self.update_url = reverse("book-update", kwargs={"pk": self.book1.pk})
        self.delete_url = reverse("book-delete", kwargs={"pk": self.book1.pk})

    # ------------------------------
    # LIST & DETAIL VIEW TESTS
    # ------------------------------

    def test_get_all_books(self):
        """Anyone can get the list of books."""
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_single_book(self):
        """Anyone can retrieve a specific book."""
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Book One")

    # ------------------------------
    # CREATE TESTS
    # ------------------------------

    def test_create_book_requires_authentication(self):
        """Unauthenticated user should NOT create a book."""
        payload = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }

        res = self.client.post(self.create_url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated user can create a book."""
        self.client.login(username="testuser", password="password123")

        payload = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }

        res = self.client.post(self.create_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ------------------------------
    # UPDATE TESTS
    # ------------------------------

    def test_update_book_requires_authentication(self):
        payload = {"title": "Updated Title"}

        res = self.client.patch(self.update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password123")

        payload = {"title": "Updated Title"}

        res = self.client.patch(self.update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # ------------------------------
    # DELETE TESTS
    # ------------------------------

    def test_delete_book_requires_authentication(self):
        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="password123")

        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ------------------------------
    # FILTER TESTS
    # ------------------------------

    def test_filter_books_by_publication_year(self):
        res = self.client.get(self.list_url + "?publication_year=2001")
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Book One")

    # ------------------------------
    # SEARCH TESTS
    # ------------------------------

    def test_search_books_by_title(self):
        res = self.client.get(self.list_url + "?search=Another")
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Another Book")

    # ------------------------------
    # ORDERING TESTS
    # ------------------------------

    def test_order_books_by_publication_year(self):
        res = self.client.get(self.list_url + "?ordering=publication_year")
        self.assertEqual(res.data[0]["publication_year"], 2001)
        self.assertEqual(res.data[1]["publication_year"], 2020)

    def test_order_books_descending(self):
        res = self.client.get(self.list_url + "?ordering=-publication_year")
        self.assertEqual(res.data[0]["publication_year"], 2020)
