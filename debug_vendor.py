
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sokohub.settings')
django.setup()

from products.models import product
from accounts.models import CustomUser

print("--- Checking Products and Vendors ---")
products = product.objects.all()
if not products.exists():
    print("No products found.")
else:
    for p in products:
        vendor = p.vendor
        print(f"Product ID: {p.id}, Name: {p.name}")
        if vendor:
            print(f"  Vendor Found: ID={vendor.id}, Username='{vendor.username}'")
        else:
            print("  NO VENDOR FOUND (Should be impossible due to foreign key constraints unless manually corrupted)")
print("--- End Check ---")
