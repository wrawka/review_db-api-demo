from rest_framework import serializers, validators
from reviews.models import Comment, Review


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

    def validate_score(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError('Оценка может быть от 1 до 10.')

    class Meta:
        model = Review
        fields = '__all__'
