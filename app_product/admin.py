from django.contrib import admin

# Register your models here.
from app_product.models import Category
from app_product.models import Brand
from app_product.models import Product
from app_product.models import Review

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Review)
