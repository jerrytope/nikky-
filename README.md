# NICKY COSMETICS - eCommerce Platform

A modern, full-featured eCommerce website for NICKY COSMETICS built with Django. This platform allows customers to browse products, add them to cart, and complete purchases with secure payment processing through Paystack.

## Features

### Customer Features
- **Product Browsing**: Browse products by category with search functionality
- **Shopping Cart**: Add/remove products, update quantities
- **User Authentication**: Sign up, login, and Google OAuth integration
- **Secure Checkout**: Complete orders with Paystack payment processing
- **Order Management**: View order history and track order status
- **Responsive Design**: Mobile-friendly interface

### Admin Features
- **Product Management**: Add, edit, and manage products with images
- **Category Management**: Organize products by categories
- **Order Management**: Process orders and update status
- **Inventory Management**: Track stock levels
- **User Management**: Manage customer accounts

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development) / PostgreSQL (production)
- **Payment**: Paystack Integration
- **Authentication**: Django Allauth with Google OAuth
- **Frontend**: Bootstrap 5, Font Awesome
- **Image Handling**: Pillow

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd tolu-website
```

### 2. Create Virtual Environment
```bash
python -m venv myenv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
myenv\Scripts\activate
```

**macOS/Linux:**
```bash
source myenv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Paystack Settings
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key

# Google OAuth Settings
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 6. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Collect Static Files
```bash
python manage.py collectstatic
```

### 9. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Configuration

### Paystack Setup
1. Sign up for a Paystack account at [paystack.com](https://paystack.com)
2. Get your API keys from the dashboard
3. Add the keys to your `.env` file

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`
6. Add the credentials to your `.env` file

## Usage

### Admin Panel
Access the admin panel at `http://127.0.0.1:8000/admin/`

1. **Add Categories**: Create product categories
2. **Add Products**: Upload product images and details
3. **Manage Orders**: Process customer orders
4. **User Management**: Manage customer accounts

### Customer Experience
1. **Browse Products**: View products by category or search
2. **Add to Cart**: Add products to shopping cart
3. **Checkout**: Complete purchase with shipping details
4. **Payment**: Pay securely through Paystack
5. **Order Tracking**: View order status and history

## Project Structure

```
tolu-website/
├── NICKY_COSMETICS/          # Main Django project
│   ├── settings.py           # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── products/                 # Products app
│   ├── models.py            # Product and Category models
│   ├── views.py             # Product views
│   ├── urls.py              # Product URLs
│   └── admin.py             # Admin configuration
├── cart/                    # Shopping cart app
│   ├── models.py            # Cart models
│   ├── views.py             # Cart views
│   ├── urls.py              # Cart URLs
│   └── context_processors.py # Cart context processor
├── orders/                  # Orders app
│   ├── models.py            # Order models
│   ├── views.py             # Order views
│   ├── urls.py              # Order URLs
│   ├── forms.py             # Order forms
│   └── admin.py             # Admin configuration
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── products/            # Product templates
│   ├── cart/                # Cart templates
│   └── orders/              # Order templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## API Endpoints

### Products
- `GET /` - Product list (homepage)
- `GET /product/<slug>/` - Product detail
- `GET /category/<slug>/` - Category products
- `GET /search/` - Product search

### Cart
- `GET /cart/` - View cart
- `POST /cart/add/<id>/` - Add to cart
- `POST /cart/update/<id>/` - Update quantity
- `POST /cart/remove/<id>/` - Remove from cart
- `POST /cart/clear/` - Clear cart

### Orders
- `GET /orders/create/` - Checkout form
- `POST /orders/create/` - Create order
- `GET /orders/payment/<id>/` - Payment page
- `GET /orders/list/` - Order history
- `GET /orders/detail/<id>/` - Order details

### Authentication
- `GET /accounts/login/` - Login page
- `GET /accounts/signup/` - Signup page
- `GET /accounts/logout/` - Logout

## Customization

### Styling
- Modify CSS variables in `templates/base.html`
- Update Bootstrap theme colors
- Customize product card layouts

### Features
- Add product reviews and ratings
- Implement wishlist functionality
- Add email notifications
- Integrate with shipping providers

## Deployment

### Production Settings
1. Set `DEBUG=False` in settings
2. Configure production database (PostgreSQL recommended)
3. Set up proper static file serving
4. Configure email settings
5. Use HTTPS for security

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Scalable cloud infrastructure

## Support

For support and questions:
- **Phone**: 08168085597
- **WhatsApp**: [WhatsApp Link](https://wa.me/2348168085597)
- **Email**: Contact through the website

## License

This project is proprietary software for NICKY COSMETICS.

## Contributing

This is a private project for NICKY COSMETICS. For feature requests or bug reports, please contact the development team. 