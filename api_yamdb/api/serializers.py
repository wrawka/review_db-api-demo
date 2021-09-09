from rest_framework import serializers

import datetime as dt

from reviews.models import Title, Genre, Category


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
    genre = GenreSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()

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



