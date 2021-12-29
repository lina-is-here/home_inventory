from datetime import date, timedelta

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from related_admin import RelatedFieldAdmin

from .models import Item, Product, Category, Location, Measurement


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Measurement)


class ExpiryDateListFilter(admin.SimpleListFilter):
    """
    Custom filter for expiry date
    """

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("expiry date")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "expiry_date"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ("exp", _("Expired")),
            ("exp_today", _("Expiring today")),
            ("exp_7", _("Expiring in the next 7 days")),
            ("exp_30", _("Expiring in the next 30 days")),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value() == "exp":
            return queryset.filter(expiry_date__lt=date.today())
        if self.value() == "exp_today":
            return queryset.filter(expiry_date=date.today())
        if self.value() == "exp_7":
            return queryset.filter(
                expiry_date__gte=date.today(),
                expiry_date__lt=date.today() + timedelta(days=7),
            )
        if self.value() == "exp_30":
            return queryset.filter(
                expiry_date__gte=date.today(),
                expiry_date__lt=date.today() + timedelta(days=30),
            )


@admin.register(Item)
class ItemAdmin(RelatedFieldAdmin):
    list_display = (
        "name",
        "location",
        "quantity",
        "measurement",
        "expiry_date",
        "name__category",
    )
    list_filter = ("location", "quantity", "name__category", ExpiryDateListFilter)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
