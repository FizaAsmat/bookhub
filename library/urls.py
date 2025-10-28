from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    borrow_book,
    return_book,
    borrowed_books_list,
    my_borrowed_books,
    available_books,
    borrowed_books
)

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),

    # Borrow / Return
    path('books/borrow/<int:book_id>/', borrow_book, name='borrow-book'),
    path('books/return/<int:book_id>/', return_book, name='return-book'),

    # Borrowed books lists
    path('borrows/all/', borrowed_books_list, name='borrowed-books-list'),
    path('borrows/mine/', my_borrowed_books, name='my-borrowed-books'),

    # Available / Borrowed books using manager with cache
    path('books/available/', available_books, name='available-books'),
    path('books/borrowed/', borrowed_books, name='borrowed-books'),
]
