from django.urls import path
from .views import ParcelAPI, CheckReceiveAPI, CheckRouteAPI, TrackAPI

urlpatterns = [
    path('parcel/', ParcelAPI.as_view(), name = 'parcel_api'),
    path('parcel/<int:pk>/', ParcelAPI.as_view(), name = 'parcel_api_with_primary_key'),
    path('check-receive/<int:pk>/', CheckReceiveAPI.as_view(), name = 'check_receive_api_with_primary_key'),
    path('check-route/<int:pk>/', CheckRouteAPI.as_view(), name = 'check_route_api_with_primary_key'),
    path('receive/', CheckReceiveAPI.as_view(), name='check_receive_api'),
    path('route/', CheckRouteAPI.as_view(), name = 'check_route_api'),
    path('track/', TrackAPI.as_view(), name = 'track_api'),
]
