from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from django.shortcuts import get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Post CRUD operations and feed.
    """
    queryset = Post.objects.all().order_by('-created_at')  
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 

    def get_permissions(self):
        """
        Allow unauthenticated users to list/retrieve posts (feed), but require auth for create/update/delete.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Automatically set the user to the authenticated user when creating a post.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='like')
    def like(self, request, pk=None):
        """
        Like a post. Prevents duplicate likes via model constraint.
        """
        post = self.get_object()
        try:
            like = Like.objects.create(post=post, user=request.user)
            serializer = LikeSerializer(like, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated], url_path='like')
    def unlike(self, request, pk=None):
        """
        Unlike a post.
        """
        post = self.get_object()
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted:
            return Response({'status': 'post unliked'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated], url_path='comments')
    def comments(self, request, pk=None):
        """
        List or create comments for a specific post.
        GET: List all comments for the post.
        POST: Create a new comment for the post.
        """
        post = self.get_object()
        if request.method == 'GET':
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)
        else:  # POST
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(post=post, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Comment CRUD operations.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically set the user to the authenticated user when creating a comment.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Optionally filter comments by post ID if provided in query params.
        """
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset