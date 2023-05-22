from groceries.models import Post, Greengrocer
from rest_framework import serializers


class GreengrocerSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Greengrocer
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    greengrocer = serializers.StringRelatedField(read_only=True)
    immage_url = serializers.ImageField()

    class Meta:
        model = Post
        fields = '__all__'        