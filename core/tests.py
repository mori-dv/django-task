from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Book


class CategoryTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category_data = {'name': 'Science'}
        self.category = Category.objects.create(name='Technology')

    def test_create_category(self):
        response = self.client.post('/categories/', self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=2).name, 'Science')

    def test_get_category(self):
        response = self.client.get(f'/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Technology')

    def test_update_category(self):
        updated_data = {'name': 'Engineering'}
        response = self.client.put(f'/categories/{self.category.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Engineering')

    def test_delete_category(self):
        response = self.client.delete(f'/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class BookTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name='Technology')
        self.category2 = Category.objects.create(name='Science')
        self.book1 = Book.objects.create(
            title='Artificial Intelligence',
            author='John McCarthy',
            description='A comprehensive guide to AI.',
            published_date='2020-01-01',
            category=self.category1
        )
        self.book2 = Book.objects.create(
            title='Machine Learning',
            author='Tom Mitchell',
            description='Introduction to ML',
            published_date='2015-01-01',
            category=self.category1
        )
        self.book3 = Book.objects.create(
            title='Quantum Physics',
            author='Albert Einstein',
            description='A foundational book on quantum physics.',
            published_date='1950-01-01',
            category=self.category2
        )

    def test_create_book(self):
        book_data = {
            'title': 'Deep Learning',
            'author': 'Ian Goodfellow',
            'description': 'Comprehensive introduction to deep learning.',
            'published_date': '2016-01-01',
            'category': self.category1.id
        }
        response = self.client.post('/books/', book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(id=4).title, 'Deep Learning')

    def test_get_book(self):
        response = self.client.get(f'/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Artificial Intelligence')

    def test_update_book(self):
        updated_data = {
            'title': 'Deep Learning',
            'author': 'Ian Goodfellow',
            'description': 'Comprehensive introduction to deep learning.',
            'published_date': '2016-01-01',
            'category': self.category1.id
        }
        response = self.client.put(f'/books/{self.book1.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Deep Learning')

    def test_delete_book(self):
        response = self.client.delete(f'/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    # New test for search functionality
    def test_search_books_by_title(self):
        response = self.client.get('/books/?search=Machine')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Machine Learning')

    def test_search_books_by_author(self):
        response = self.client.get('/books/?search=Einstein')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Albert Einstein')

    # test for filtering
    def test_filter_books_by_category(self):
        response = self.client.get(f'/books/?category={self.category1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only two books in category1
        titles = [book['title'] for book in response.data]
        self.assertIn('Artificial Intelligence', titles)
        self.assertIn('Machine Learning', titles)

    # Test for search and filter together
    def test_search_and_filter_books(self):
        response = self.client.get(f'/books/?category={self.category1.id}&search=Machine')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Machine Learning')