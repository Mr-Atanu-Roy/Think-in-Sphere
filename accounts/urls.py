from django.urls import path
from .views import *

urlpatterns = [
    path('signin/', signin, name="signin"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    
    path('dashboard/', dashboard, name="dashboard"),
    
    path('email-verification/', email_verification, name="email-verification"),
    path('reset-password/', reset_password, name="reset-password"),
    
    
    path('dashboard/get-query-search-result/', SearchQueryView.as_view(), name="get-query-search-result"),
]
