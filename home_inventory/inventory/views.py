import datetime

from django.shortcuts import render

from .models import Item, Location, Category
from .forms import ItemForm


def get_location_context(location_id):
    location = Location.objects.get(id=location_id)
    categories = Category.objects.all()
    rows = []
    for category in categories:
        items = Item.objects.filter(location=location, name__category=category)
        if items:
            rows.append({"category": category, "items": items})
    print(rows)
    return {"location_id": location_id, "location": location, "rows": rows}


def index(request):
    """Index view."""
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
            }
        )

    context = {"rows": rows}
    return render(request, "index.html", context=context)


def location_detail(request, location_id):
    """Detail view of the location"""
    context = get_location_context(location_id)
    return render(request, "location-detail.html", context=context)


def add_item(request, location_id):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.location = Location.objects.get(id=location_id)
            new_item.save()
            return render(
                request,
                "location-detail.html",
                context=get_location_context(location_id),
            )
    else:
        form = ItemForm()
        print("CALLING GET")
    return render(
        request, "add_item.html", context={"form": form, "location_id": location_id}
    )
