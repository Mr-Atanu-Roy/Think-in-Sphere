from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard-search-history/', SearchQueryView.as_view(), name="dashboard-search-history"),
]
