from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('products/', views.admin_products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/', views.view_product, name='view_product'),
    path('categories/', views.admin_categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('orders/', views.admin_orders, name='orders'),
    path('users/', views.admin_users, name='users'),
] 