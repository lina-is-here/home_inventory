from django.contrib import admin
from related_admin import RelatedFieldAdmin

from .models import Item, Product, Category, Location, Measurement


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Measurement)


@admin.register(Item)
class ItemAdmin(RelatedFieldAdmin):
    list_display = ("name", "location", "quantity", "measurement", "expiry_date",
                    "name__category")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
