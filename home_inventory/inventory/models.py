import datetime
from datetime import date

from django.db import models

from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    """Model representing a category of the product, e.g. Sweets"""

    name = models.CharField(
        max_length=200, unique=True, help_text="The product category"
    )
    slugify_name = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.slugify_name = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Model representing a product to store, e.g. Tomato paste"""

    name = models.CharField(
        max_length=200, unique=True, help_text="Name of the product"
    )
    slugify_name = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.slugify_name = slugify(self.name)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    """Model representing a location to store items, e.g. Pantry"""

    name = models.CharField(
        max_length=200, unique=True, help_text="Location, e.g. Pantry"
    )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """Returns the URL to access a particular location"""
        return reverse("location-detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Measurement(models.Model):
    """Model representing measurement of the item, e.g. Pieces"""

    name = models.CharField(max_length=100, unique=True, help_text="Measurement unit")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Item(models.Model):
    """Model representing a stored item"""

    name = models.ForeignKey(Product, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    expiry_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    measurement = models.ForeignKey(Measurement, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "location", "expiry_date"],
                name="unique product - location - expiry date",
            )
        ]

    @property
    def is_expired(self):
        # if the expiry_date is None, item is non-expirable
        if self.expiry_date:
            return self.expiry_date < date.today()

    @property
    def is_expiring_soon(self):
        # if the expiry_date is None, item is non-expirable
        if self.expiry_date:
            return self.expiry_date < (date.today() + datetime.timedelta(days=7))

    def get_absolute_url(self):
        """Returns the URL to access a particular item"""
        return reverse("item-detail", args=[str(self.id)])

    def __str__(self):
        return self.name.name
