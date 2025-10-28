from django.contrib import admin
from .models import Book, Borrow

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_available')

@admin.register(Borrow)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrow_date', 'return_date','is_returned')
