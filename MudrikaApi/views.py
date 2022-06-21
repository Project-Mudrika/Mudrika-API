from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework import generics
from .models import Sudu
from .serializer import subscriberserializer, suduserializer
# Create your views here.


class SuduListAPIView(generics.ListAPIView):

    serializer_class = suduserializer

    def get_queryset(self):
        return Sudu.objects.all()


def ExampleView(request):
    example_id = request.GET.get('walletid', '')
    new_var = {
        "wallet_id_return_value": example_id
    }
    return JsonResponse(new_var)
