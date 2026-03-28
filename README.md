# AuraBazaar

A Django-based e-commerce web application.

## Tech Stack

- Python 3.10+
- Django 5.1
- Bootstrap 5
- SQLite (dev) / configurable for production
- WhiteNoise for static file serving

## Local Setup

### 1. Clone the repo

git clone https://github.com/AtharvaP555/AuraBazaar.git
cd AuraBazaar/ecp

### 2. Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # Mac/Linux

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up environment variables

Copy .env.example to .env and fill in your values:
cp .env.example .env

### 5. Run migrations

python manage.py migrate

### 6. Create a superuser

python manage.py createsuperuser

### 7. Run the development server

python manage.py runserver

## Environment Variables

| Variable      | Description                   |
| ------------- | ----------------------------- |
| SECRET_KEY    | Django secret key             |
| ALLOWED_HOSTS | Comma-separated allowed hosts |

## Git Workflow

This project uses conventional commits:

- `fix:` bug fixes
- `security:` security improvements
- `feat:` new features
- `perf:` performance improvements
- `chore:` maintenance tasks
