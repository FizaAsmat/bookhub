# BookHub 📚

A Django REST Framework project for managing a library system with Redis + Celery integration.

## Features
- User authentication and role-based access
- Borrow and return books
- Celery task reminders for due books
- PostgreSQL + Redis backend

## Apps

This project consist of 2 apps mainly:

- library (handle books)
- - borrow books
- - return books

- accounts (mainly handle roles)
- - admin
- - librarian
- - public
