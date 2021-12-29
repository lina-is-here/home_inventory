from django.contrib import admin
from .models import Item, Product, Category, Location, Measurement


admin.site.register(Item)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Measurement)
