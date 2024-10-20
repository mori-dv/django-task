from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, unique=True, related_name='books')
    description = models.TextField(null=True, blank=True)
    published_date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.name
