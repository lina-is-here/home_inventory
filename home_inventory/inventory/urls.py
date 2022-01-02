from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("locations/<int:location_id>/", views.location_detail, name="location-detail"),
    path("locations/<int:location_id>/add/", views.add_item, name="add-item"),
    path("items/<int:item_id>/", views.item_detail, name="item-detail"),
    path("items/<int:item_id>/edit/", views.edit_item, name="edit-item"),
    path("items/<int:item_id>/delete/", views.delete_item, name="delete-item"),
]
