from rest_framework import serializers, validators
from users.models import User, Code, CHOICES
from reviews.models import Comment, Review, Title, Genre, Category
import datetime as dt


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


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

    class Meta:
        model = Review
        fields = '__all__'


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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        # genres = []
        # for genre in response['genre']:
        #     pass
        #     # print(dir(GenreSerializer(genre)))
        #     print(GenreSerializer(genre).data)
        # print('!')
        return response

    # def to_internal_value(self, data):
    #     self.fields['slug'] = serializers.SlugRelatedField(
    #         queryset=Category.objects.all(),
    #         slug_field='slug'
    #     )
    #     return super(TitleSerializer, self).to_internal_value(data)


    def get_score(self, obj):
        pass
