from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(
        r"^product-autocomplete/$",
        views.ProductAutoComplete.as_view(),
        name="product-autocomplete",
    ),
    path("locations/<int:location_id>/", views.location_detail, name="location-detail"),
    path("locations/<int:location_id>/add/", views.add_item, name="add-item"),
    path("items/<int:item_id>/", views.item_detail, name="item-detail"),
    path("items/<int:item_id>/edit/", views.edit_item, name="edit-item"),
    path("items/<int:item_id>/delete/", views.delete_item, name="delete-item"),
]
