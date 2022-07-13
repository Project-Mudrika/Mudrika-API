from django.urls import path
from .views import *


urlpatterns = [
    path('example/', fetch_all_user_data, name="example"),
    path('fetch-user-data/', fetch_user_data, name="fetch_user_data"),
    path('register/', register_new_user, name="fetch_user_data"),
    path('new-access-token/', generate_new_access_token, name='new_access_token')
]
