from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(
        r"^product-autocomplete/$",
        views.ProductAutoComplete.as_view(create_field="name"),
        name="product-autocomplete",
    ),
    re_path(
        r"^category-autocomplete/$",
        views.CategoryAutoComplete.as_view(create_field="name"),
        name="category-autocomplete",
    ),
    path(
        "product/<str:product_name>/",
        views.get_product,
        name="get-product",
    ),
    path(
        "product-barcode/<str:barcode>/",
        views.get_product_by_barcode,
        name="get-product-by-barcode",
    ),
    path(
        "slugify/<str:text>/",
        views.get_slugified,
        name="get-slugified",
    ),
    path(
        "slugify/",
        views.get_slugified,
        name="get-slugified",
    ),
    path("locations/<int:location_id>/", views.location_detail, name="location-detail"),
    path("locations/add/", views.add_location, name="add-location"),
    path("locations/<int:location_id>/add/", views.add_item, name="add-item"),
    path("items/<int:item_id>/edit/", views.edit_item, name="edit-item"),
    path("items/<int:item_id>/delete/", views.delete_item, name="delete-item"),
]
