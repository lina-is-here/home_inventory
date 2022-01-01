import datetime

from django.shortcuts import render

from .models import Item, Location


def index(request):
    """Index view."""
    rows = []
    locations = Location.objects.all()

    for location in locations:
        rows.append(
            {
                "location": location.name,
                "items_count": Item.objects.filter(location=location).count(),
                "items_expired": Item.objects.filter(
                    location=location, expiry_date__lt=datetime.date.today()
                ).count(),
            }
        )

    context = {"rows": rows}
    return render(request, "index.html", context=context)
