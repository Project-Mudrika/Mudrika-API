import json
import random
import string

from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

from .models import AccessLevelTokenDummy, Sudu, UserProfileDummy
from .forms import AccessLevelForm
from .serializer import subscriberserializer, suduserializer
from .supabase_client import *

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
        return JsonResponse({"Error in Request": e}, status=400)
    else:
        if acc_id:
            data = json.loads(fetch_single_user_data(acc_id).json())
            return JsonResponse(data)
        else:
            return JsonResponse({"data": "Account ID (Wallet ID) not provided"}, status=400)


@csrf_exempt
def register_new_user(request):

    if request.method == "POST":
        received_payload = json.loads(request.body)
        print(received_payload)
    else:
        return JsonResponse({"response": "Invalid Request. Send POST request only to /register"}, status=400)
    try:
        payload = {'accid': '123', 'level': "district", 'fname': "arya",
                   'lname': "sreejith", 'state': "kerala", 'district': "tvm", 'username': "arya"}

    except Exception as e:
        raise e
        # return Response(data={"Data": "Add Employee  Failed", "Error": str(r.status_code)}, status=status.HTTP_201_CREATED)
    # Payload format
    #  {'accid': acid, 'level': level, 'fname': fnam, 'lname': lnam, 'state': sta, 'district': dis, 'username': user}
    return JsonResponse(received_payload)


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser])
def generate_new_access_token(request, format=None):
    if request.method == "POST":
        form_obj = AccessLevelForm(request.POST)
        if form_obj.is_valid():
            new_access_token = ''.join(random.choices(string.ascii_uppercase +
                                                      string.digits, k=20))

            print(new_access_token)

            response_obj = form_obj.cleaned_data
            response_obj['access_phrase'] = new_access_token

            newAccessLevelToken = AccessLevelTokenDummy(**response_obj)
            newAccessLevelToken.save()
            return JsonResponse(response_obj)
        else:
            form_error = form_obj.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"response": "Invalid Request. Send POST request only to /new-access-token"}, status=400)


@api_view(["GET"])
def get_access_level(request):
    try:
        access_level_token = request.GET.get("token", "")
    except Exception as e:
        return JsonResponse({"Error": e}, status=400)
    else:
        if access_level_token:
            access_level = AccessLevelTokenDummy.objects.filter(
                access_phrase=access_level_token).values()[0]
            return JsonResponse(access_level, safe=False)
        else:
            return JsonResponse({"Error": "Access Key Not Provided"}, status=400)
