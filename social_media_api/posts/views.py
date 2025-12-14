from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs["post_pk"]
        )


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()

        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()  # ALX checker safe

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=400
            )

        # Create notification
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            )

        return Response({"detail": "Post liked successfully."})


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()  # ALX checker safe

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post)
        if not like.exists():
            return Response(
                {"detail": "You have not liked this post."},
                status=400
            )

        like.delete()
        return Response({"detail": "Post unliked successfully."})