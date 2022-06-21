from django.shortcuts import render
from rest_framework import generics
from .models import Sudu
from .serializer import subscriberserializer, suduserializer
# Create your views here.


class SuduListAPIView(generics.ListAPIView):

    serializer_class = suduserializer

    def get_queryset(self):
        return Sudu.objects.all()
