from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard-search-history/', DashboardSearchQueryView.as_view(), name="dashboard-search-history"),
    path('course-search/', CourseSerchQueryView.as_view(), name="course-search"),
]
