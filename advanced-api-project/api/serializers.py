from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# Serializer for Book. Handles validation & field serialization.
class BookSerializer(serializers.ModelSerializer):

    # Custom validation for publication_year
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields: title, year, author
        

# Serializer for Author with nested list of books.
class AuthorSerializer(serializers.ModelSerializer):

    # Nest all related books dynamically using BookSerializer
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
        # books field shows all Book objects linked via "related_name='books'"
