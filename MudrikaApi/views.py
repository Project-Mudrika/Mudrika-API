import os
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.core import serializers

from rest_framework import generics
from .models import UserProfileDummy, Sudu
from .serializer import subscriberserializer, suduserializer
# Create your views here.


class SuduListAPIView(generics.ListAPIView):

    serializer_class = suduserializer

    def get_queryset(self):
        print(Sudu.objects.all())
        return Sudu.objects.all()


def ExampleView(request):
    example_id = request.GET.get('walletid', '')
    user = UserProfileDummy.objects.filter(acc_address=example_id).values()[0]
    # new_var = {
    # "wallet_id_return_value": example_id,
    # "user": name

    # }
    return JsonResponse(user, safe=False)
