from django.urls import path
from .views import *


urlpatterns = [
    path('', SuduListAPIView.as_view(), name='mudrika'),
    path('example/', fetch_all_user_data, name="example"),
    path('fetch-user-data/', fetch_user_data, name="fetch_user_data"),
]
