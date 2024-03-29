import json
import random
import string
import pyqrcode

from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

from .models import AccessLevelTokenData, UserProfileSignUpData
from .forms import AccessLevelForm, SignUpForm, ConsignmentForm, VolunteerSignUpForm, VolunteerActivityForm
from .supabase_client import *
from .contract_client import *

# Create your views here.


def fetch_all_user_data(request):
    example_id = request.GET.get('walletid', '')
    user = UserProfileSignUpData.objects.filter(
        walletid=example_id).values()[0]
    # new_var = {
    # "wallet_id_return_value": example_id,
    # "user": name

    # }

    return JsonResponse(user, safe=False)


def fetch_user_data(request):
    try:
        acc_id = request.GET.get("walletId", "")
        usr_type = json.loads(fetch_type(acc_id))["data"][0]["sub_category"]

        data = None
        if usr_type == "authority":
            if acc_id:
                data = json.loads(fetch_single_user_data(acc_id).json())
        if usr_type == "driver":
            if acc_id:
                data = json.loads(fetch_single_driver_data(acc_id).json())
        if usr_type == "volunteer":
            if acc_id:
                data = json.loads(fetch_single_volunteer_data(acc_id).json())

        return JsonResponse({"walletId": acc_id, "type": usr_type,
                             **data})

    except Exception as e:
        return JsonResponse({"Error in Request": str(e)}, status=400, safe=False)


def fetch_national_officer_data(request):
    try:
        return JsonResponse({"data": get_national_officers()})
    except Exception as e:
        return JsonResponse({"Error in Request": e}, status=400)


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser])
def generate_new_access_token(request):
    """
    Function to generate various authority level based access tokens for completing the sign up of users
    """
    if request.method == "POST":
        access_form = AccessLevelForm(request.POST)
        if access_form.is_valid():
            new_access_token = ''.join(random.choices(string.ascii_uppercase +
                                                      string.digits, k=20))
            response_obj = access_form.cleaned_data
            response_obj['access_phrase'] = new_access_token

            try:
                insert_into_access_level(**response_obj)
                return JsonResponse(response_obj)

            except Exception as e:
                return JsonResponse(str(Exception), status=400)

        else:
            form_error = access_form.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"response": "Invalid Request. Send POST request only to /new-access-token"}, status=400)


@csrf_exempt
def register_new_officer(request):

    if request.method == "POST":
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            # sign up form data
            # {
            #   "walletid": "577g9H03rH09kT6hf",
            #   "first_name": "Sudev",
            #   "last_name": "Suresh Sreedevi",
            #   "username": "sudevssuresh",
            #   "access_level_token": "7687yodf08ha"
            # }
            access_level_token = sign_up_form.cleaned_data["access_level_token"]
            access_level = get_access_level(
                access_level_token).get('access_level')

            if not access_level:
                return JsonResponse({"error": "Access Key Invalid or Not Found"}, status=400)

            response_obj = sign_up_form.cleaned_data
            name = response_obj['first_name'] + response_obj['last_name']

            # store the user details into the database
            insert_into_db_officer(
                walletid=response_obj.get('walletid'),
                level=access_level,
                state=response_obj.get('state'),
                district=response_obj.get('district'),
                fname=response_obj.get('first_name'),
                lname=response_obj.get('last_name')
            )
            # insert_into_account(
            #     walletid=response_obj.get('walletid'),
            #     sub_category=response_obj.get('sub_category')
            # )
            # add the user access details into contract
            add_user_contract(
                account_id=response_obj['walletid'], access_level=access_level, name=name)

            # response_obj = {**response_obj, **access_level}
            remove_access_key(access_level_token)

            return JsonResponse(response_obj)
        else:
            form_error = sign_up_form.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"error": "Invalid Request. Send POST request only to /register/officer/"}, status=400)

        # payload = {'walletid': '123', 'level': "district", 'fname': "arya",
        #            'lname': "sreejith", 'state': "kerala", 'district': "tvm", 'username': "arya"}


@csrf_exempt
def register_new_volunteer(request):
    if request.method == "POST":
        sign_up_form = VolunteerSignUpForm(request.POST)
        if sign_up_form.is_valid():
            print(f"Cleaned Data: {sign_up_form.cleaned_data}")

            insert_into_db_volunteer(**sign_up_form.cleaned_data)

            return JsonResponse(sign_up_form.cleaned_data, status=200)
        else:
            form_error = sign_up_form.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"error": "Invalid Request. Send POST request only to /register/volunteer/"}, status=400)


def fetch_driver_data(request):
    try:
        acc_add = request.GET.get("account_address", "")
    except Exception as e:
        return JsonResponse({"Error in Response", e}, status=400)
    else:
        if acc_add:
            data = json.loads(fetch_single_driver_data(acc_add).json())
            return JsonResponse(data)
        else:
            return JsonResponse({"data": "Account ID (Wallet ID) not provided"}, status=400)


# @csrf_exempt
# def register_new_driver(request):

#     if request.method == "POST":
#         sign_up_form = SignUpForm(request.POST)
#         if sign_up_form.is_valid():
#             # sign up form data
#             # {
#             #   "walletid": "577g9H03rH09kT6hf",
#             #   "first_name": "Sudev",
#             #   "last_name": "Suresh Sreedevi",
#             #   "username": "sudevssuresh",
#             #   "access_level_token": "7687yodf08ha"
#             # }
#             access_level_token = sign_up_form.cleaned_data["access_level_token"]
#             access_level = get_access_level(
#                 access_level_token).get('access_level')

#             if not access_level:
#                 return JsonResponse({"error": "Access Key Invalid or Not Found"}, status=400)

#             response_obj = sign_up_form.cleaned_data
#             name = response_obj['first_name'] + response_obj['last_name']

#             # store the user details into the database
#             insert_into_db(
#                 walletid=response_obj.get('walletid'),
#                 username=response_obj.get('username'),
#                 level=access_level,
#                 state=response_obj.get('state'),
#                 district=response_obj.get('district'),
#                 fname=response_obj.get('first_name'),
#                 lname=response_obj.get('last_name')
#             )

#             # add the user access details into contract
#             add_user_contract(
#                 account_id=response_obj['walletid'], access_level=access_level, name=name)

#             # response_obj = {**response_obj, **access_level}
#             remove_access_key(access_level_token)

#             return JsonResponse(response_obj)
#         else:
#             form_error = sign_up_form.errors
#             return JsonResponse(form_error, status=400)
#     else:
#         return JsonResponse({"error": "Invalid Request. Send POST request only to /register"}, status=400)


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser])
def new_consignment(request):

    if request.method == 'POST':
        consignment_form = ConsignmentForm(request.POST)
        if consignment_form.is_valid():
            # New Consignment form data
            # {
            #   "cons_id" : "23480j04",
            #   "con_name" : "Food",
            #   "quantity" : "4 quintels",
            #   "location" : "Kozhikode",
            #   "sender": "2935405I09405940I4W0G8HRW"
            #   "receiver": "054UTG094TG09EJR094RU30GJ"
            # }
            consignment_data = consignment_form.cleaned_data
            insert_into_consignment(
                cons_id=consignment_data.get("cons_id"),
                con_name=consignment_data.get("con_name"),
                location=consignment_data.get("location"),
                quantity=consignment_data.get("quantity"),
                sender=consignment_data.get("sender"),
                # sender is the current holder when consignment is newly created
                curr_holder=consignment_data.get("sender"),
                receiver=consignment_data.get("receiver"),
            )
            qr_string = consignment_data["cons_id"] + ";" + \
                consignment_data["sender"] + ";" + consignment_data["receiver"]
            print(consignment_data)
            print(qr_string)
            qr_image = pyqrcode.create(qr_string)
            return JsonResponse({"data": {"qr": qr_image.png_as_base64_str(scale=8)}})
        else:
            form_error = consignment_form.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"error": "Invalid Request. Send POST request only"}, status=400)


@csrf_exempt
def add_new_volunteer_activity(request):
    if request.method == "POST":
        new_activity_form = VolunteerActivityForm(request.POST)
        print(new_activity_form)
        print(f"Cleaned Data: {new_activity_form.cleaned_data}")
        if new_activity_form.is_valid():
            print(f"Cleaned Data: {new_activity_form.cleaned_data}")

            add_activity_to_volunteer(**new_activity_form.cleaned_data)

            return JsonResponse(new_activity_form.cleaned_data, status=200)
        else:
            form_error = new_activity_form.errors
            return JsonResponse(form_error, status=400)
    else:
        return JsonResponse({"error": "Invalid Request. Send POST request only to /volunteer/new-activity/"}, status=400)


def fetch_volunteer_activity(request):
    try:
        walletid = request.GET.get("walletId", "")
    except Exception as e:
        return JsonResponse({"Error in Response", e}, status=400)
    else:
        if walletid:
            data = json.loads(fetch_activity_from_volunteer(walletid).json())
            return JsonResponse(data)
        else:
            # data = json.loads(fetch_all_volunteer_activites().json())
            data = fetch_all_volunteer_activites()
            return JsonResponse(data)
