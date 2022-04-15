from django.urls import path
from .views import ParcelAPI, CheckReceiveAPI, CheckRouteAPI, TrackAPI

urlpatterns = [
    path('parcel/', ParcelAPI.as_view()),
    path('parcel/<int:pk>/', ParcelAPI.as_view()),
    path('check-receive/<int:pk>/', CheckReceiveAPI.as_view()),
    path('check-route/<int:pk>/', CheckRouteAPI.as_view()),
    path('receive/', CheckReceiveAPI.as_view()),
    path('route/', CheckRouteAPI.as_view()),
    path('track/', TrackAPI.as_view()),
]
