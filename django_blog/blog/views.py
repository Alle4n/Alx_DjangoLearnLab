from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Comment


# ================================
# AUTHENTICATION VIEWS
# ================================
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created! Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("post-list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


@login_required
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        messages.success(request, "Profile updated.")

    return render(request, "blog/profile.html")


# ================================
# CRUD VIEWS (POSTS)
# ================================
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "Create"
        return ctx


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "Edit"
        return ctx


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Create Comment (handled on Post Detail page)
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post-detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/comment_form.html", {"form": form, "action": "Add Comment"})


# Update Comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()


# Delete Comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()
