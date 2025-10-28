from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Custom QuerySet for Book (chainable)
class BookQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True)

    def borrowed(self):
        return self.filter(is_available=False)


# Custom Managers
class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def borrowed(self):
        return self.get_queryset().borrowed()

class BorrowManager(models.Manager):
    def active(self):
        return self.filter(is_returned=False)

    def overdue(self):
        today = date.today()
        return self.filter(is_returned=False, return_date__lt=today)


# Models
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    is_available = models.BooleanField(default=True)

    objects = BookManager()  # custom manager with chainable queryset

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    objects = BorrowManager()  # simple manager, no custom queryset
