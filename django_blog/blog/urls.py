from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    # Authentication
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),

    # CRUD - corrected singular URLs
    path("", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]

# Comment URLs
path("post/<int:pk>/comment/new/", add_comment, name="comment-add"),
path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
