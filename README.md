# Complaint Management System (Django)

This project is a Django-based Complaint Management System that allows users to create and manage complaints. It uses PostgreSQL as the backend database and includes basic machine learning dependencies for future enhancements.

---

## Prerequisites

Make sure you have the following installed on your system:

- Python (3.8 or above)
- pip (Python package manager)
- PostgreSQL
- pgAdmin 4

---

## Setup Instructions

### 1. Install Required Python Packages

Install Django and other required dependencies using pip:

```
pip install django
pip install scikit-learn
pip install joblib
```

---

## Database Setup (PostgreSQL)

### 2. Install PostgreSQL

- Download and install PostgreSQL.
- During installation:
  - Set a username and password for the PostgreSQL server.
  - Keep the default port as 5432.

### 3. Install pgAdmin 4

- Install pgAdmin 4.
- Connect pgAdmin to the PostgreSQL server using the credentials created during installation.

### 4. Create Database

- Create a new database named:

```
combat
```

---

## Django Configuration

Update the `settings.py` file with PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'combat',
        'USER': '<your_postgres_username>',
        'PASSWORD': '<your_postgres_password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Run Database Migrations

Run the following commands to create database tables:

```
python manage.py makemigrations
python manage.py migrate
```

---

## Run the Server

Start the Django development server:

```
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

---

## Notes

- Make sure PostgreSQL service is running before starting the server.
- Using a virtual environment is recommended.
- This project can be extended with authentication and ML-based complaint analysis.

## API Endpoints (Postman Collection Reference)

This project exposes REST APIs for user management and complaint management using Django and JWT-based authentication.

---

### 1. Create User

**Endpoint**
POST /api/create_user

**Description**
Creates a new user in the system.

**Request Body (JSON)**
{
  "username": "sam",
  "first_name": "sam1",
  "last_name": "singh",
  "email": "sam@gmail.com",
  "password": "sam@123"
}

---

### 2. User Login

**Endpoint**
POST /api/user_login

**Description**
Authenticates the user and returns a JWT token.

**Request Body (JSON)**
{
  "username": "sam",
  "password": "sam@123"
}

**Response**
{
  "token": "<JWT_TOKEN>"
}

---

### 3. Create Complaint (Protected)

**Endpoint**
POST /api/create_complaint

**Authentication**
Bearer Token (JWT)

**Request Body (JSON)**
{
  "title": "Water Leakage",
  "description": "There is water leakage near A building on the ground floor and it should be addressed immediately.",
  "status": "pending",
  "priority": "high"
}

**Response**
{
  "complaint_id": 1,
  "message": "Complaint created"
}

---

### 4. Get Complaints (Protected)

**Endpoint**
GET /api/get_complaint

**Authentication**
Bearer Token (JWT)

**Response**
[
  {
    "id": 1,
    "title": "Water Leakage",
    "description": "There is water leakage near A building...",
    "status": "pending",
    "priority": "high"
  }
]

---

### 5. Update Complaint Status (Protected)

**Endpoint**
POST /api/update_complaint_status

**Authentication**
Bearer Token (JWT)

**Request Body (JSON)**
{
  "complaint_id": 1,
  "status": "resolved"
}

**Response**
{
  "message": "Complaint status updated successfully"
}

---

## Authentication Flow Summary

1. Create user
2. Login and get JWT token
3. Use token as Bearer Token for complaint APIs

---

## Notes

- All protected APIs require a valid JWT token
- Tested using Postman

## Background Status Update Explanation

The complaint status update process is handled automatically in the background using **Django signals** and **threading** to ensure a smooth and non-blocking user experience.

### How It Works

- Whenever a complaint is saved in the database, a **Django `post_save` signal** is triggered.
- This signal listens for any save operation on the Complaint model (both create and update).
- As soon as the complaint is saved, the system immediately updates the complaint status to **`in_progress`**.

### Asynchronous Status Update Using Threading

- After updating the status to `in_progress`, a **separate thread** is created using Python threading.
- This thread runs as a background process and updates the complaint status to **`resolved`** after a defined delay.
- Threading is used to ensure that the user does **not have to wait** for the delay to complete in order to receive the complaint ID or API response.
- This makes the status update process **asynchronous**, improving performance and user experience.

### Preventing Infinite Signal Loops

- Since updating the model inside a `post_save` signal will trigger the signal again, a safety check is required.
- The `created` flag provided by Django signals is used to identify whether the object is newly created.
- If `created` is `True`, the background update logic is executed.
- If `created` is `False`, the signal logic is skipped.
- This prevents **re-execution of the signal** and avoids an **infinite loop** caused by repeated `post_save` triggers.

### Summary

- `post_save` signal listens for complaint save events
- Status is immediately set to `in_progress`
- Background thread updates status to `resolved`
- Threading ensures non-blocking execution
- Signal flags prevent infinite loops

This approach ensures efficient, asynchronous processing of complaint status updates without affecting API response time.

