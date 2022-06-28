from django.urls import path
from .views import *


urlpatterns = [
    path('', SuduListAPIView.as_view(), name='mudrika'),
    path('example/', ExampleView, name="example"),
]
