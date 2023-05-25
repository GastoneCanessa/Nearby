from groceries.models import Post, Greengrocer
from rest_framework import serializers


class GreengrocerSerializer(serializers.ModelSerializer):

    location = serializers.SerializerMethodField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Greengrocer
        fields = '__all__'

    def get_location(self, instance):
        return (instance.location.coords, instance.location.srid)


class PostSerializer(serializers.ModelSerializer):

    greengrocer = serializers.StringRelatedField(read_only=True)
    immage_url = serializers.ImageField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'        

    
class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["immage_url"]
