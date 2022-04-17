from django.urls import path
from .views import UsersAPI, CurrentUserAPI

urlpatterns = [
    path('', UsersAPI.as_view(), name= 'user_api'),
    path('current-user', CurrentUserAPI.as_view(), name = 'current_user_api'),
    path('<int:pk>/', UsersAPI.as_view(), name = 'user_api_with_primary_key'),
]
