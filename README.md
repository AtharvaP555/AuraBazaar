# AuraBazaar

AuraBazaar is an e-commerce platform built using Django, designed to offer a seamless shopping experience. The project includes essential e-commerce features like product browsing, searching, checkout, order tracking, and contact forms.

## Features
- Home page displaying product categories
- Product details page with "Add to Cart" and "Buy Now" options
- Search functionality to find products
- Contact page for customer inquiries
- Order tracking system
- Checkout system with form validation
- Shopping cart with local storage functionality
- Django-based backend with a MySQL database

## Tech Stack
- **Frontend**: HTML, CSS, Bootstrap, JavaScript, jQuery
- **Backend**: Django (Python), MySQL
- **Database**: MySQL
- **Deployment**: Django development server (can be hosted on platforms like AWS, Heroku, or PythonAnywhere)

## Installation & Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AuraBazaar.git
   cd AuraBazaar
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser for Admin Panel**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open your browser and visit: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure
```
AuraBazaar/
│── ecp/                 # Main Django project folder
│── shop/                # Django app handling e-commerce functionality
│   ├── migrations/      # Database migrations
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   ├── models.py        # Database models
│   ├── views.py         # Backend logic
│   ├── urls.py          # URL routing
│── media/               # User-uploaded images (if applicable)
│── db.sqlite3           # Default Django database (change to MySQL in production)
│── manage.py            # Django project management script
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License.

## Author
Developed by **AtharvaP555**

