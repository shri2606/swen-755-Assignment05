# Secure Session Management Project

## Overview

This project demonstrates secure session management in a web application prototype. The focus is on implementing session tracking, authentication, and authorization. The prototype simulates a blogging platform where authenticated and authorized users can create, edit, and view posts, while unauthorized users have limited access.

## Features

1. **Session Tracking**:

   - A session is created for every authenticated user.
   - Session identifiers are stored in the database to maintain user sessions.

2. **Authentication**:

   - Django's built-in authentication system is used.
   - Users must log in to access restricted features.

3. **Authorization**:

   - Users have different permissions based on their roles.
   - Only authorized users can be able to access the administration page.

4. **CRUD Operations for Blog Posts**:
   - Create, view, edit, and delete blog posts.
   - Posts can be saved as drafts or published.

## Project Structure

```plaintext
blog-app/
├── blog/                     # Main application logic
│   ├── admin.py              # Admin interface configurations
│   ├── apps.py               # Application configuration
│   ├── forms.py              # Forms for posts and comments
│   ├── migrations/           # Database migrations
│   ├── models.py             # Models for Post and Comment
│   ├── templates/            # HTML templates for the app
│   │   ├── blog/             # Templates for blog views
│   │   └── registration/     # Templates for authentication (login/logout)
│   ├── tests.py              # Unit tests
│   ├── urls.py               # URL routing for the application
│   ├── views.py              # Views handling the request-response cycle
│   └── __init__.py           # Initialization file
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
└── mysite/                   # Project configuration and settings
```

## Frameworks and Tools Used

- **Django:** Web framework for rapid development and secure web apps.
- **SQLite:** Lightweight database for development.

## Architectural Breakers Identified

### **1. Session Expiration Vulnerability**

Our analysis revealed a deficiency in session expiration mechanisms, allowing user sessions to persist indefinitely without adequate timeout controls. This vulnerability increases the risk of session hijacking and unauthorized access, especially in cases of shared or unattended devices, posing a serious threat to user data security. The absence of session timeout mechanisms further exacerbates this risk.

### **2. Cross-Site Request Forgery (CSRF) Protection Gap**

The project contains forms that handle user input but lacks robust CSRF protection in some views. This vulnerability could allow attackers to execute unauthorized actions using a user’s active session, compromising data integrity and trust.

### **3. Cookie Security Vulnerabilities**

The current cookie management strategy does not enforce secure transmission (`SESSION_COOKIE_SECURE`) or client-side access restrictions (`SESSION_COOKIE_HTTPONLY`). These vulnerabilities leave session cookies susceptible to interception and manipulation, potentially enabling attackers to hijack sessions and gain unauthorized access to sensitive resources.

### **4. Access Control Limitations**

The project’s access control implementation relies on basic authentication checks (`@login_required`) without enforcing role-based permissions. This could allow authenticated users to access resources or perform actions beyond their intended authorization level, increasing the risk of data breaches.

## Architectural Breaker Demonstrated

### **Session Expiration Vulnerability**

1. A **successful test case**, where proper session expiration logic is implemented, ensuring inactive sessions are invalidated and unauthorized access is prevented.
2. A **failing test case**, where the absence of session expiration logic allows sessions to remain active indefinitely, demonstrating the architectural breaker in action.

### **Access Control Limitations**

1.A **successful test case**, where strict access control ensures that only superusers can access the admin page, while normal users and unauthenticated users are redirected.

This demonstration underscores the importance of implementing robust session timeout mechanisms to ensure secure session management.

## How to Run the Project:

- **Install Dependencies:**

````
cd blog-app
python -m venv myenv
source myenv/bin/activate  # On Windows: `myenv\Scripts\activate`
pip install django```

````

- **Run Migrations:** Set up the database:

```
python manage.py migrate
```

- **Create Superuser:**

```
python manage.py createsuperuser
```

- **Run the Server:** Start the development server

```
python manage.py runserver
```
