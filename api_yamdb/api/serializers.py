import datetime as dt

from rest_framework import serializers, validators, exceptions
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CHOICES, Code, User


class SelfSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
        read_only_fields = ('role',)
        model = User


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        read_only_fields = ('role',)
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
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='id')

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', default=serializers.CurrentUserDefault())
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id', default=0)

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError('Оценка может быть от 1 до 10.')
        return value

    def validate(self, attrs):
        title = self.context.get('view').kwargs.get('title_id')
        review = Review.objects.filter(title=title, author=self.context['request'].user)
        if self.context['request'].method == 'POST' and review.exists():
            raise exceptions.ValidationError('You already have a review on this title')
        return super().validate(attrs)


class GenreSerializer(serializers.ModelSerializer):
    queryset = Genre.objects.all()

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(), slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.datetime.today().year
        if not value <= year:
            raise serializers.ValidationError('Год не может быть будущим!')
        return value

    def to_representation(self, instance):
        title = super().to_representation(instance)
        title['genre'] = GenreSerializer(instance.genre, many=True).data
        title['category'] = CategorySerializer(instance.category, source=title).data
        return title

    def get_rating(self, obj):
        reviews = [review.score for review in obj.reviews.all()]
        if reviews:
            return round(sum(reviews)/len(reviews))
        else:
            return None
