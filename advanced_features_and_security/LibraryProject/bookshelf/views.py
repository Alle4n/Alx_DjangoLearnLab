from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import  ExampleForm, BookForm 


# -------------------------------
# Book Views
# -------------------------------
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@login_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


# -------------------------------
# ExampleForm View
# -------------------------------
@login_required
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Example: process form data safely
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # You could save this to DB or send email, etc.
            return redirect('book_list')  # redirect after successful submission
    else:
        form = ExampleForm()
    return render(request, "bookshelf/example_form.html", {"form": form})
