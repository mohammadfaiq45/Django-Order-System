import os
import django
import random
from uuid import uuid4

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderSystem.settings')
django.setup()

from users.models import User
from products.models import Product
from orders.models import Order, OrderItem

print("Seeding Users...")

admin_user, created = User.objects.get_or_create(
    email='admin@example.com',
    defaults={'is_admin': True, 'name': 'Admin User'}
)
if created:
    admin_user.set_password('123456')
    admin_user.save()

customer_names = ['Aliya', 'Sara', 'Ahmed', 'Fatima']
for name in customer_names:
    user, created = User.objects.get_or_create(
        email=f'{name.lower()}@example.com',
        defaults={'name': name, 'is_admin': False}
    )
    if created:
        user.set_password('123456')
        user.save()

print("Seeding Products...")
product_names = [
    ('Laptop', 10),
    ('Phone', 25),
    ('Headphones', 50),
    ('Monitor', 15)
]

for name, qty in product_names:
    Product.objects.get_or_create(
        name=name,
        defaults={
            'description': f'{name} description',
            'visibility': True,
            'available_units': qty
        }
    )

print("Seeding Orders...")
customers = User.objects.filter(is_admin=False)
products = list(Product.objects.all())

for customer in customers:
    if Order.objects.filter(user=customer).exists():
        continue

    order = Order.objects.create(
        user=customer,
        address=f'123 {customer.name} Street',
        phone_no='03001234567',
        special_instructions='N/A',
        status='pending'
    )
    for _ in range(random.randint(1, 3)):
        product = random.choice(products)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=random.randint(1, 3)
        )

print("Seeding complete!")
