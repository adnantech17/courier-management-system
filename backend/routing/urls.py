from django.urls import path
from .views import BranchAPI, BranchEdgeAPI

urlpatterns = [
    path('edge/', BranchEdgeAPI.as_view(), name = 'branch_edge_api'),
    path('edge/<int:pk>/', BranchEdgeAPI.as_view(), name = 'branch_edge_api_with_primary_key'),
    path('branch/', BranchAPI.as_view(), name='branch_api'),
    path('branch/<int:pk>/', BranchAPI.as_view(), name = 'branch_api_with_primary_key'),
]
