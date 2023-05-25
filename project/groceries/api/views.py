from groceries.api.serializers import (
    GreengrocerSerializer, 
    PostSerializer, 
    PostImageSerializer
)
from groceries.models import Greengrocer, Post
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly
    )
from groceries.api.permissions import IsAuthorOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404


class GreengrocerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    queryset = Greengrocer.objects.all()
    serializer_class = GreengrocerSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        review_queryset = Greengrocer.objects.filter(user=user)
        if review_queryset.exists():
            raise ValidationError("Hai gia creato un venditore!")
        serializer.save(user=user)


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        review_queryset = Greengrocer.objects.get(user=user)
        serializer.save(greengrocer=review_queryset)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)     


class PostimmageUpdateView(generics.UpdateAPIView):
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get("pk")
        # post_object = Post.objects.get(id=pk)
        post_object = get_object_or_404(Post, pk=pk)
        return post_object


class LogoutVieSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

