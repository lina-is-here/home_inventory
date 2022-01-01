import datetime

from django.shortcuts import render

from .models import Item, Location, Category


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
    location = Location.objects.get(id=location_id)
    categories = Category.objects.all()
    rows = []
    for category in categories:
        items = Item.objects.filter(location=location, name__category=category)
        if items:
            rows.append({"category": category,
                         "items": items})

    context = {"location_id": location_id,
               "location": location,
               "rows": rows}
    return render(request, "location-detail.html", context=context)
