# Job Posting Portal (Backend API)

A production-level Django REST Framework backend designed for a Job Portal system. This project supports different user roles (Employer, Job Seeker) and provides a highly-optimized SQLite-to-PostgreSQL backend with robust validation and permissions.

## Features

* **Custom Authentication System**: Django REST Framework token authentication handling diverse registration validation rules.
* **Role-Based Access Control**: Strict segregation between Employers (who post jobs) and Job Seekers (who apply to jobs).
* **Database Optimization**: PostgreSQL database model design using efficient relation queries, `unique_together` constraints, and optimized fields.
* **REST Constraints / Logic**: Robust `ModelViewSet` and `GenericAPIView` structures with DRF pagination and exception handling.
* **Advanced Search API**: Integrated search and filtering (`django_filters`) for finding jobs using parameters like salary, job_type, title, company, skills, or location.

## Technology Stack

* **Language**: Python 3
* **Framework**: Django 4.x
* **API Framework**: Django REST Framework (DRF)
* **Database**: PostgreSQL (`psycopg2-binary`)

## Setup Instructions

**1. Create & activate a Virtual Environment:**
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

**2. Install Requirements:**
```bash
pip install -r requirements.txt
```

**3. Configure PostgreSQL Database:**
Open `job_portal/settings.py` and modify `DATABASES` with your actual local PostgreSQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'job_portal_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**4. Run Database Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Start Development Server:**
```bash
python manage.py runserver
```

## API Endpoint Guide (Postman Testing)

### General / Auth
* **`POST /api/register/`** - Register a generic new user (`Job Seeker` or `Employer`).
* **`POST /api/login/`** - Login and receive an auth token with User JSON response.

### Core Features (Jobs & Applications)
* **`GET /api/jobs/`** - Fetch all job posts. Search/Filter via query string (e.g., `?location=NY`).
* **`POST /api/jobs/create/`** - **(Employer Only)** Create a new job post.
* **`POST /api/apply/`** - **(Job Seeker Only)** Apply to an outstanding job via ID and document attachment.

*(Full REST Router endpoints still available mapped under standard `/api/v1/auth/` and `/api/v1/` routes for robust standard production integrations).*

## Code Quality Highlights

* Well-documented Model Viewsets and Authentication API views.
* Robust Serializer-level validation ensuring tight security controls for User and Application creation constraints.
* Clean and distinct separation between applications (`jobs` and `users`) keeping concerns isolated based on standard Django recommendations.
