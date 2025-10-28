# 📚 Library Management API

A Django REST Framework project for managing books and borrowings with:

✅ Role-based access control (Admin, Librarian, Member)  
🔐 JWT authentication  
⚡ Redis caching  
⏱️ Celery for background tasks  
💾 PostgreSQL database  

---

## 🚀 Features

- User authentication with JWT  
- Role-based permissions (`IsAdmin`, `IsLibrarian`, `Member`)  
- CRUD for books (Admin & Librarian only)  
- Borrow / Return books (Authenticated users)  
- Redis caching for book and borrow lists  
- Celery integration for async/background tasks (like reminders, cleanup)

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository
```bash

git clone https://github.com/your-username/library_project.git
cd library_project
```
## Create and activate virtual environment
```bash

python -m venv venv
source venv/bin/activate
```
## Install Dependencies
```bash

pip install -r requirements.txt
```
## Database Setup


## Apply Database Migrations
```bash

python manage.py makemigrations
python manage.py migrate
```
## Create SuperUser
```bash

python manage.py createsuperuser
```
## Run Django Server
```bash

python manage.py runserver
```
Visit the app at:
http://127.0.0.1:8000/

## Start Redis Server
```bash

redis-server
```
## Run Celery Worker
```bash

celery -A library_project worker --loglevel=info
```
## Obtain Access Token

Endpoint:
POST /api/token/

- Request Body:
```json
{
  "username": "yourusername",
  "password": "yourpassword"
}
```
- Response:
```json
{
  "access": "<ACCESS_TOKEN>",
  "refresh": "<REFRESH_TOKEN>"
}
```
- Include this header for protected endpoints:
Authorization: 
Bearer <ACCESS_TOKEN>

- Refresh Access Token

Endpoint:
POST /api/token/refresh/
- Request Body:
```json
{
  "refresh": "<REFRESH_TOKEN>"
}
```
## API endpoints
| Method        | Endpoint                 | Description                | Permission          |
| ------------- | ------------------------ | -------------------------- | ------------------- |
| **GET**       | `/api/books/`            | List all books             | Anyone              |
| **POST**      | `/api/books/`            | Add a new book             | Admin / Librarian   |
| **PUT/PATCH** | `/api/books/<id>/`       | Update a book              | Admin / Librarian   |
| **DELETE**    | `/api/books/<id>/`       | Delete a book              | Admin / Librarian   |
| **POST**      | `/api/borrow/<book_id>/` | Borrow a book              | Authenticated users |
| **POST**      | `/api/return/<book_id>/` | Return a borrowed book     | Authenticated users |
| **GET**       | `/api/my-borrows/`       | View user’s borrowed books | Authenticated users |
| **GET**       | `/api/borrowed-books/`   | View all borrowed books    | Admin / Librarian   |

## Redis Caching
Redis is used to cache data like:
- Book lists
- Borrowed book lists (per user)

This improves performance and reduces redundant database queries.
## How It Works
When books are fetched for the first time:
- Data is retrieved from the database and stored in Redis.
- Next time the same endpoint is called, data comes directly from Redis (cache hit).

When a book is borrowed or returned:
- Cache is invalidated to keep data fresh.
```python
cache.delete('books_available')
cache.delete('books_borrowed')
cache.delete('borrows_active')
```

## Common Commands
| Command                                            | Description                     |
| -------------------------------------------------- | ------------------------------- |
| `python manage.py makemigrations`                  | Create migration files          |
| `python manage.py migrate`                         | Apply migrations                |
| `python manage.py runserver`                       | Start Django development server |
| `python manage.py createsuperuser`                 | Create admin user               |
| `celery -A library_project worker --loglevel=info` | Run Celery worker               |
| `celery -A library_project beat --loglevel=info`   | Run Celery beat scheduler       |

## Folder Structure
```bash
library_project/
│
├── accounts/
│   ├── models.py          # Profile with role (Admin/Librarian/Member)
│   ├── permissions.py     # Custom permission classes
│   ├── serializers.py
│   ├── views.py
│
├── library/
│   ├── models.py          # Book, Borrow models with managers & querysets
│   ├── views.py           # Role-based + Redis caching views
│   ├── serializers.py
│   ├── urls.py
│
├── library_project/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py          # Celery configuration
│   └── __init__.py
│
├── manage.py
├── requirements.txt
└── README.md
```
---
## Workflow
- Run Redis Server
- Run django server
- run celery worker
- Test endpoints with Postman:
- - Obtain JWT token from /api/token/
- - Use Authorization: Bearer <ACCESS_TOKEN> in headers
- - Test borrowing, returning, and viewing
- --
## Tech Stack
| Component          | Technology            |
| ------------------ | --------------------- |
| **Backend**        | Django 5.2            |
| **API Framework**  | Django REST Framework |
| **Authentication** | JWT (SimpleJWT)       |
| **Database**       | PostgreSQL            |
| **Cache / Broker** | Redis                 |
| **Async Tasks**    | Celery                |
| **Environment**    | Python 3.11+          |

## Notes
- Ensure Redis server is running before Celery.
- JWT tokens expire — refresh using /api/token/refresh/.
- Cache clears automatically on borrow/return.
- Only Admins and Librarians can modify books.
- Regular users can only borrow/return their own books.
