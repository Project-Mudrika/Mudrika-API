import json
import random
import string

from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

from .models import AccessLevelTokenData, Sudu, UserProfileSignUpData
from .forms import AccessLevelForm, SignUpForm
from .serializer import subscriberserializer, suduserializer
from .supabase_client import *

# Create your views here.


# class SuduListAPIView(generics.ListAPIView):

#     serializer_class = suduserializer

#     def get_queryset(self):
#         print(Sudu.objects.all())
#         return Sudu.objects.all()


def fetch_all_user_data(request) -> JsonResponse:
    example_id = request.GET.get('walletid', '')
    user = UserProfileSignUpData.objects.filter(
        acc_address=example_id).values()[0]
    # new_var = {
    # "wallet_id_return_value": example_id,
    # "user": name

    # }

    return JsonResponse(user, safe=False)


def fetch_user_data(request) -> JsonResponse:
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
@api_view(["POST"])
@parser_classes([MultiPartParser])
def generate_new_access_token(request) -> JsonResponse:
    if request.method == "POST":
        access_form = AccessLevelForm(request.POST)
        if access_form.is_valid():
            new_access_token = ''.join(random.choices(string.ascii_uppercase +
                                                      string.digits, k=20))
            response_obj = access_form.cleaned_data
            response_obj['access_phrase'] = new_access_token

            newAccessLevelToken = AccessLevelTokenData(**response_obj)
            newAccessLevelToken.save()
            return JsonResponse(response_obj)
        else:
            form_error = access_form.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"response": "Invalid Request. Send POST request only to /new-access-token"}, status=400)


def get_access_level(request, internal_call: bool = False, access_level_token: str = None) -> (dict | JsonResponse):
    if internal_call:
        try:
            access_level = AccessLevelTokenData.objects.filter(
                access_phrase=access_level_token).values()[0]
            return access_level
        except:
            return {}
    else:
        try:
            access_level_token = request.GET.get("token", "")
        except Exception as e:
            return JsonResponse({"Error": e}, status=400)
        else:
            if access_level_token:
                try:
                    access_level = AccessLevelTokenData.objects.filter(
                        access_phrase=access_level_token).values()[0]
                    return JsonResponse(access_level)
                except:
                    return JsonResponse({"Error": "Access Key Not Found"}, status=404)
            else:
                return JsonResponse({"Error": "Access Key Not Provided"}, status=400)


@csrf_exempt
def register_new_user(request) -> JsonResponse:

    if request.method == "POST":
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            # sign up form data
            # {
            #   "acc_address": "577g9H03rH09kT6hf",
            #   "first_name": "Sudev",
            #   "last_name": "Suresh Sreedevi",
            #   "username": "sudevssuresh",
            #   "access_level_token": "7687yodf08ha"
            # }
            access_level_token = sign_up_form.cleaned_data["access_level_token"]
            access_level = get_access_level(request, True, access_level_token)
            if access_level == {}:
                return JsonResponse({"error": "Access Key Invalid or Not Found"}, status=400)

            response_obj = sign_up_form.cleaned_data

            # Removing access level token and token creation time from response object
            del response_obj["access_level_token"]
            del access_level["access_phrase"]
            del access_level["created_at"]

            response_obj = {**response_obj, **access_level}

            return JsonResponse(response_obj)
        else:
            form_error = sign_up_form.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"error": "Invalid Request. Send POST request only to /register"}, status=400)

        # payload = {'accid': '123', 'level': "district", 'fname': "arya",
        #            'lname': "sreejith", 'state': "kerala", 'district': "tvm", 'username': "arya"}
