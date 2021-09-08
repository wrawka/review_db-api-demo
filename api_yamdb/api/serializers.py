from django.contrib.auth import get_user_model
from reviews.models import Comment, Review
from rest_framework import serializers, validators

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='pk')
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='pk')

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='pk')

    class Meta:
        model = Review
        fields = '__all__'