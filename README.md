# 📚 BookHub

BookHub is a **Django REST Framework** project for managing a digital library system.  
It includes **role-based access**, **Celery + Redis integration**, and **PostgreSQL** as the database.

---

## 🚀 Features

- 🔐 **User Authentication & Role-Based Access**
  - Admin and Librarian have separate permissions.
- 📖 **Book Management**
  - Borrow and return books easily through APIs.
- ⏰ **Celery Background Tasks**
  - Automated reminders for borrowed books.
- 💾 **PostgreSQL + Redis Backend**
  - Redis used for caching and Celery task queue.

---

## 🧩 Project Structure

This project consists of two main Django apps:

### **1️⃣ library app**
Handles:
- Adding and listing books
- Borrowing and returning books
- Celery reminder tasks for due returns

### **2️⃣ accounts app**
Handles:
- User creation and role management (Admin, Librarian, Public)
- Authentication and permissions

---

## ⚙️ Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Backend | Django, Django REST Framework |
| Database | PostgreSQL |
| Caching & Queue | Redis + Celery |
| Authentication | Role-based access via DRF permissions |
| Environment | Python 3, Virtualenv |

---

## 🧠 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/FizaAsmat/bookhub.git
cd bookhub
