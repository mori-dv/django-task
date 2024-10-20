from rest_framework.serializers import ModelSerializer

from core.models import Book, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
