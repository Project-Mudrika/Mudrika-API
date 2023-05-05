import json
import os
from supabase import create_client, Client
import datetime

from dotenv import load_dotenv
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def insert_into_access_level(access_level, state, district, access_phrase):
    """
    Insert access level data into db
    """
    data = locals()
    # this creates a dict with the function params
    res = supabase.table('AccessLevelTokenData').insert(
        data).execute()
    return res


def insert_into_consignment(cons_id, con_name, quantity, location, sender, curr_holder, receiver):
    """
    Insert consignment details into db
    """
    data = locals()  # this creates a dict with the function params
    res = supabase.table('consignments').insert(
        data).execute()

    return res


def get_access_level(access_phrase):
    """
    Checks the access level of user from access token returns empty dict if it doesn't exist
    """
    data = supabase.table('AccessLevelTokenData').select(
        'access_level').eq('access_phrase', access_phrase).execute()

    if data.data != []:
        return data.data[0]
    else:
        return {}


def remove_access_key(access_phrase):
    """
    Removes the access token from db after it has been used for sign up
    """
    res = supabase.table('AccessLevelTokenData').delete().eq(
        'access_phrase', access_phrase).execute()

    return res


def insert_into_db_officer(walletid, level, fname, lname, state, district):
    payload = locals()

    data = supabase.table('authority').insert(
        payload).execute()
    return data


def insert_into_account(walletid, sub_category):
    payload = locals()

    data = supabase.table('account').insert(
        payload).execute()
    return data


def insert_into_db_volunteer(walletid, aadharngoid, name, profileimg, voltype, about="", activities=[""]):
    payload = {
        'walletid': walletid,
        'aadharngoid': aadharngoid,
        'name': name,
        'profileimg': profileimg,
        'voltype': voltype,
        'about': about,
        'activities': activities,
    }

    data = supabase.table('volunteer').insert(payload).execute()
    return data


def add_activity_to_volunteer(walletid, username, description, date, imageLink):
    new_activity = {
        "walletid": walletid,
        "username": username,
        "description": description,
        "date": date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "imageLink": imageLink,
    }

    current_array_data = fetch_activity_from_volunteer(walletid)
    current_array = json.loads(current_array_data.json())[
        'data'][0]['activities']

    if current_array == [""]:
        current_array = []

    data = supabase.table('volunteer').update(
        {"activities": [new_activity] + current_array}).eq("walletid", walletid).execute()
    return data


def fetch_activity_from_volunteer(walletid):
    data = supabase.table('volunteer').select(
        'activities').eq('walletid', walletid).execute()
    return data

def fetch_all_volunteer_activites():
    result = supabase.table('volunteer').select("walletid, activities").execute()

# Group activities by volunteer
    volunteer_activities = {}
    for volunteer in result.data:
        walletid = volunteer.get("walletid")
        activities = volunteer.get("activities", [])
        volunteer_activities[walletid] = activities

    # Print volunteer activities
    return volunteer_activities


def insert_into_db_driver(received_payload):
    data = supabase.table('driver').insert(received_payload).execute()
    return data


def fetch_all_data():
    data = supabase.table('authority').select(
        'walletid', 'level', 'fname', 'lname', 'state', 'district').execute()
    print(data)
    print('\n')
    return data


def fetch_all_driver_data():
    data = supabase.table('driver').select('wallet_id', 'created_at', 'first_name',
                                           'last_name', 'state', 'district', 'mobile_number').execute()
    print(data)
    print('\n')
    return data


def fetch_single_user_data(walletid):
    data1 = supabase.table('authority').select(
        'walletid,level,fname,lname,state,district').eq('walletid', walletid).execute()
    # assert len(data.get("data", [])) > 0
    print(data1)
    return data1


def fetch_type(walletid):
    response = supabase.table('account').select(
        'sub_category').eq('walletid', walletid).execute()
    json_string = response.json()
    data = json.loads(json_string)
    return json_string


def fetch_single_driver_data(walletid):
    data1 = supabase.table('driver').select(
        'walletid,first_name,last_name,state,district,mobile_number').eq('walletid', walletid).execute()
    print(data1)
    return data1


def fetch_single_volunteer_data(walletid):
    data1 = supabase.table('volunteer').select(
        'walletid,aadharngoid,name,profileimg,voltype').eq('walletid', walletid).execute()
    print(data1)
    return data1


def get_national_officers():
    officers = supabase.table('authority').select(
        'walletid, fname, lname').eq('level', 'national').execute()
    return list(officers)[0][1]
