from rest_framework import serializers
from .models import Author, Message


class AuthorSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = Author
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    pdf_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = "__all__"
