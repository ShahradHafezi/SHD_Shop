# SHD Shop

یک پروژه ساده فروشگاهی با Django REST Framework.

## امکانات

- Product CRUD
- Search و Filter محصولات
- Signup و Signin
- Token و JWT Authentication
- Profile CRUD
- Basket و Purchase
- Zarinpal Sandbox
- Management command برای داده نمونه
- Swagger و ReDoc

## نصب و اجرا

```bash
python -m venv .venv
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## مستندات API

- Swagger: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## مسیرهای اصلی

```text
POST   /api/v1/auth/signup/
POST   /api/v1/auth/signin/
POST   /api/v1/auth/jwt/
POST   /api/v1/auth/jwt/refresh/
GET    /api/v1/profile/
GET    /api/v1/products/
GET    /api/v1/products/{slug}/
GET    /api/v1/basket/
POST   /api/v1/basket/items/
GET    /api/v1/orders/
POST   /api/v1/orders/
POST   /api/v1/orders/{id}/pay/
GET    /api/v1/payments/verify/
```

برای درخواست‌های JWT از هدر زیر استفاده کنید:

```text
Authorization: Bearer <access_token>
```

پرداخت به‌صورت پیش‌فرض روی محیط Sandbox زرین‌پال تنظیم شده است.
