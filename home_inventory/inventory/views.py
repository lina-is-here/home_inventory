import datetime
import json

from dal import autocomplete
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from slugify import slugify

from .models import Item, Location, Category, Product
from .forms import ItemForm, LocationForm, EditItemForm, AddItemForm


class CustomComplete(autocomplete.Select2QuerySetView):
    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get("page_obj", None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

            # Don't offer to create a new option if slugified name already exists
            existing_options = (
                slugify(self.get_result_label(result))
                for result in context["object_list"]
            )
            if slugify(q) in existing_options:
                display_create_option = False

        if display_create_option and self.has_add_permission(self.request):
            create_option = [
                {
                    "id": q,
                    "text": _('Create "%(new_value)s"') % {"new_value": q},
                    "create_id": True,
                }
            ]
        return create_option


class ProductAutoComplete(CustomComplete):
    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Product.objects.all()

        if self.q:
            slug_q = slugify(self.q)
            qs = qs.filter(slugify_name__icontains=slug_q)

        return qs


class CategoryAutoComplete(CustomComplete):
    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Category.objects.all()

        if self.q:
            slug_q = slugify(self.q)
            qs = qs.filter(slugify_name__icontains=slug_q)

        return qs


def get_product(request, product_name):
    product = Product.objects.get(name__icontains=product_name)
    return HttpResponse(
        json.dumps(
            {
                "category_id": product.category.id,
                "category_name": product.category.name,
                "barcode": product.barcode,
            }
        )
    )


def get_product_by_barcode(request, barcode):
    try:
        product = Product.objects.get(barcode=barcode)
        response = json.dumps({"id": product.id, "name": product.name})
    except Product.DoesNotExist:
        response = ""
    return HttpResponse(response)


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
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                "location-detail.html",
                context=get_location_context(location_id),
            )
    else:
        form = AddItemForm(
            initial={"location": default_location},
        )
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
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return render(
                request,
                "location-detail.html",
                context=get_location_context(item.location.id),
            )
    else:
        form = EditItemForm(
            instance=item,
            initial={"category": item.name.category, "barcode": item.name.barcode},
        )
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
