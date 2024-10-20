from rest_framework import viewsets, status, filters
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer


class BookPagination(PageNumberPagination):
    # we can change it to 10 or more
    page_size = 5


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Category.DoesNotExist:
            raise NotFound(detail="Category not found.", code=status.HTTP_404_NOT_FOUND)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']

    # this is for bonus: Filtering by category and search
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)  # Filter by category
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(detail="Invalid data provided. Please check your input.",
                                  code=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Book.DoesNotExist:
            raise NotFound(detail="The book you are looking for does not exist.", code=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            raise ValidationError(detail=e.detail, code=status.HTTP_400_BAD_REQUEST)
