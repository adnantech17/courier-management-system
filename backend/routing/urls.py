from django.urls import path
from .views import BranchAPI, BranchEdgeAPI

urlpatterns = [
    path('edge/', BranchEdgeAPI.as_view()),
    path('edge/<int:pk>/', BranchEdgeAPI.as_view()),
    path('branch/', BranchAPI.as_view()),
    path('branch/<int:pk>/', BranchAPI.as_view()),
]
