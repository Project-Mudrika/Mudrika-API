from django.urls import path
from .views import *


urlpatterns = [
    # path('', SuduListAPIView.as_view(), name='mudrika'),
    path('example/', fetch_all_user_data, name="example"),
    path('fetch-user-data/', fetch_user_data, name="fetch_user_data"),
    path('register/', register_new_user, name="register"),
    path('new-access-token/', generate_new_access_token, name='new_access_token'),
    path('get-access-level/', get_access_level, name="get_access_level")
]
