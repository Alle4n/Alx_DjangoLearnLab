from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # ✅ import the views module

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Use built-in class-based views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Use views.register explicitly
    path('register/', views.register, name='register'),
]
