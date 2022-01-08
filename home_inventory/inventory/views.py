import datetime
import json

from dal import autocomplete
from django.http import HttpResponse
from django.shortcuts import render

from .models import Item, Location, Category, Product
from .forms import ItemForm, LocationForm


class ProductAutoComplete(autocomplete.Select2QuerySetView):
    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class CategoryAutoComplete(autocomplete.Select2QuerySetView):
    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Category.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


def get_product_category(request, product_name):
    product = Product.objects.get(name__icontains=product_name)

    return HttpResponse(
        json.dumps({"id": product.category.id, "name": product.category.name})
    )


def get_location_context(location_id):
    location = Location.objects.get(id=location_id)
    categories = Category.objects.all()
    rows = []
    for category in categories:
        items = Item.objects.filter(location=location, name__category=category)
        if items:
            rows.append({"category": category, "items": items})
    return {"location_id": location_id, "location": location, "rows": rows}


def get_index_context():
    rows = []
    locations = Location.objects.all()

    for location in locations:
        rows.append(
            {
                "location": location,
                "items_count": Item.objects.filter(location=location).count(),
                "items_expired": Item.objects.filter(
                    location=location, expiry_date__lt=datetime.date.today()
                ).count(),
                "items_expiring_soon": Item.objects.filter(
                    location=location,
                    expiry_date__gte=datetime.date.today(),
                    expiry_date__lt=datetime.date.today() + datetime.timedelta(days=7),
                ).count(),
            }
        )

    return {"rows": rows}


def index(request):
    """Index view."""
    context = get_index_context()
    return render(request, "index.html", context=context)


def location_detail(request, location_id):
    """Detail view of the location"""
    context = get_location_context(location_id)
    return render(request, "location-detail.html", context=context)


def add_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                "index.html",
                context=get_index_context(),
            )
    else:
        form = LocationForm()
    return render(
        request,
        "add_location.html",
        context={"form": form},
    )


def add_item(request, location_id):
    default_location = Location.objects.get(id=location_id)
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                "location-detail.html",
                context=get_location_context(location_id),
            )
    else:
        form = ItemForm(initial={"location": default_location})
    return render(
        request,
        "edit_item.html",
        context={
            "form": form,
            "location_id": location_id,
            "location": default_location,
            "action": "add",
        },
    )


def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return render(
                request,
                "location-detail.html",
                context=get_location_context(item.location.id),
            )
    else:
        form = ItemForm(instance=item, initial={"category": item.name.category})
    return render(
        request,
        "edit_item.html",
        context={"form": form, "item_id": item_id, "item": item, "action": "edit"},
    )


def delete_item(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(id=item_id)
        location_id = item.location.id
        item.delete()
        return render(
            request,
            "location-detail.html",
            context=get_location_context(location_id),
        )
