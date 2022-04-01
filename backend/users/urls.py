from django.urls import path
from .views import UsersAPI

urlpatterns = [
    path('', UsersAPI.as_view()),
    path('<int:pk>/', UsersAPI.as_view()),
]
