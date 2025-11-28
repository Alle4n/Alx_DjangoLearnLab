from django.db import models

# Author model stores simple information about the writer.
# One author can have many books.
class Author(models.Model):
    name = models.CharField(max_length=255)  # Name of the author

    def __str__(self):
        return self.name


# Book model holds book details.
# It is linked to Author through a ForeignKey (one-to-many).
class Book(models.Model):
    title = models.CharField(max_length=255)  # Title of the book
    publication_year = models.IntegerField()  # Year book was published
    author = models.ForeignKey(
        Author,
        related_name='books',   # Allows nested serialization (author.books)
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
