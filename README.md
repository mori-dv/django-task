# Book and Category CRUD API with Django REST Framework

## Introduction
This project is a RESTful API built using Django and Django REST Framework (DRF) to manage a collection of books. Each book belongs to a specific category, and users can perform CRUD (Create, Read, Update, Delete) operations on both books and categories.

## Features
- **CRUD Operations**: Full CRUD functionality for both books and categories.
- **Pagination**: Book list is paginated with 5 items per page.
- **Filtering**: Books can be filtered by category using the `category` query parameter.
- **Search**: Books can be searched by title or author using the `search` query parameter.
- **Error Handling**: Proper error handling for invalid data and resources not found (404 and 400 errors).

## API Endpoints

### Category Endpoints
- **GET /categories/**: List all categories.
- **POST /categories/**: Create a new category.
- **GET /categories/{id}/**: Retrieve a specific category by ID.
- **PUT /categories/{id}/**: Update an existing category.
- **DELETE /categories/{id}/**: Delete a category.

### Book Endpoints
- **GET /books/**: List all books (with pagination, filtering, and search support).
- **POST /books/**: Create a new book.
- **GET /books/{id}/**: Retrieve a specific book by ID.
- **PUT /books/{id}/**: Update an existing book.
- **DELETE /books/{id}/**: Delete a book.

### Query Parameters
- **Search**: You can search books by title or author using the `?search=` query parameter.
  - Example: `/books/?search=Artificial`
- **Filter by Category**: You can filter books by category using the `?category=` query parameter.
  - Example: `/books/?category=1`
- **Combined Search and Filter**: You can combine search and filter together.
  - Example: `/books/?category=1&search=Learning`

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/mori-dv/django-task.git
cd django-task
