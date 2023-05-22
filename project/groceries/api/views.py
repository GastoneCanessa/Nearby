from groceries.api.serializers import GreengrocerSerializer, PostSerializer
from groceries.models import Greengrocer, Post
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
    )
from groceries.api.permissions import IsAuthorOrReadOnly
from rest_framework.exceptions import ValidationError


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
    permission_classes = [IsAuthorOrReadOnly]

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
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        review_queryset = Greengrocer.objects.get(user=user)
        serializer.save(greengrocer=review_queryset)

     