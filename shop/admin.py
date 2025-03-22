from django.contrib import admin
from shop.models import Catalogs, Categories, UnderCategories, \
    Products, Orders, Carts

admin.site.register(Catalogs)
admin.site.register(Categories)
admin.site.register(UnderCategories)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Carts)
