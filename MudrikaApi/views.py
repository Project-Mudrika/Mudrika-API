from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.core import serializers

from rest_framework import generics
from .models import UserProfileDummy, Sudu
from .serializer import subscriberserializer, suduserializer
from .supabase_client import *
import json
# Create your views here.


class SuduListAPIView(generics.ListAPIView):

    serializer_class = suduserializer

    def get_queryset(self):
        print(Sudu.objects.all())
        return Sudu.objects.all()


def fetch_all_user_data(request):
    example_id = request.GET.get('walletid', '')
    user = UserProfileDummy.objects.filter(acc_address=example_id).values()[0]
    # new_var = {
    # "wallet_id_return_value": example_id,
    # "user": name

    # }

    return JsonResponse(user, safe=False)


def fetch_user_data(request):
    try:
        acc_id = request.GET.get("walletid", "")
    except Exception as e:
        raise e
    else:
        if acc_id:
            data = json.loads(fetch_single_user_data(acc_id).json())
            return JsonResponse(data)
        else:
            return JsonResponse({"data": "Account ID (Wallet ID) not provided"}, status=400)


def register_new_user(request):
    # Payload format
    #  {'accid': acid, 'level': level, 'fname': fnam, 'lname': lnam, 'state': sta, 'district': dis, 'username': user}
    return None
