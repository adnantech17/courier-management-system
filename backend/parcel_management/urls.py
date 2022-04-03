from django.urls import path
from .views import ParcelAPI

urlpatterns = [
    path('parcel/', ParcelAPI.as_view()),
    path('parcel/<int:pk>/', ParcelAPI.as_view()),
]
