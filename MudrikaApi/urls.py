from django.urls import path
from .views import *


urlpatterns = [
    path('example/', fetch_all_user_data, name="example"),
    path('fetch-user-data/', fetch_user_data, name="fetch_user_data"),
    path('fetch-national-officers/', fetch_national_officer_data,
         name="fetch_national_officers"),
    path('register/officer/', register_new_officer, name="registerOfficer"),
    path('register/volunteer/', register_new_volunteer, name="registerVolunteer"),
    path('new-access-token/', generate_new_access_token, name='new_access_token'),
    path('new-consignment/', new_consignment, name='new_consignment'),
    path('volunteer/new-activity/',
         add_new_volunteer_activity, name='new_activity'),
    path('volunteer/fetch-activities/',
         fetch_volunteer_activity, name='fetch_activities'),
]
