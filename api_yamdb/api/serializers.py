import datetime as dt

from rest_framework import serializers, validators
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CHOICES, Code, User


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


class UserSerializerWithoutRole(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = User


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = Code


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
        return value

    class Meta:
        model = Review
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(), slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'score')

    def validate_year(self, value):
        year = dt.datetime.today().year
        if not value <= year:
            raise serializers.ValidationError('Год не может быть будущим!')
        return value

    def get_score(self, obj):

        pass
