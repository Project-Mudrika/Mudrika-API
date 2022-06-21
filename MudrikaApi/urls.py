from django.urls import path
from .views import SuduListAPIView

urlpatterns = [
    path('mudrika/', SuduListAPIView.as_view(), name='mudrika')
]
