import os
from supabase import create_client, Client

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


def insert_into_db_officer(accid, level, fname, lname, state, district, username):
    payload = locals()

    data = supabase.table('authority').insert(
        payload).execute()
    return data

def insert_into_account(walletid,sub_category):
    payload = locals()

    data = supabase.table('account').insert(
        payload).execute()
    return data


def insert_into_db_volunteer(walletid, aadharngoid, name, profileimg, voltype,about,activities):
    payload = {
        'walletid': walletid,
        'aadharngoid': aadharngoid,
        'name': name,
        'profileimg': profileimg,
        'voltype': voltype,
        'about':about,
        'activities': activities,
 }

    data = supabase.table('volunteer').insert(payload).execute()
    return data


def insert_into_db_driver(received_payload):
    data = supabase.table('driver').insert(received_payload).execute()
    return data


def fetch_all_data():
    data = supabase.table('authority').select(
        'accid', 'level', 'fname', 'lname', 'state', 'district', 'username').execute()
    print(data)
    print('\n')
    return data


def fetch_all_driver_data():
    data = supabase.table('driver').select('wallet_id', 'created_at', 'first_name',
                                           'last_name', 'state', 'district', 'mobile_number').execute()
    print(data)
    print('\n')
    return data


def fetch_single_user_data(accid):
    data1 = supabase.table('authority').select(
        'accid,level,fname,lname,state,district, username').eq('accid', accid).execute()
    # assert len(data.get("data", [])) > 0
    print(data1)
    return data1

def fetch_type(accid):
    datat = supabase.table('account').select ('sub_category').eq('accid',accid).execute()
    return datat

def fetch_single_driver_data(walletid):
    data1 = supabase.table('driver').select(
        'wallet_id,first_name,last_name,state,district,mobile_number').eq('wallet_id', walletid).execute()
    print(data1)
    return data1

def fetch_single_volunteer_data(walletid):
    data1 = supabase.table('volunteer').select(
        'walletid,aadharngoid,name,state,profileimg,voltype').eq('wallet_id', walletid).execute()
    print(data1)
    return data1

# insert_into_db("1010","national","Neeraj","Krishna","Kerala","klm","neerajkrishna")
# fetch_all_data()

    # insert_into_db("1009", "national", "Devu", "diya", "kerala", "tvm", "devudiya")
    # fetch_all_data()

    # data = supabase.table('authority').select('accid').execute()
    # print(data)
    # data = supabase.table('authority').insert({'accid': '1335', 'fname': "aarya" }).execute()
    # assert if insert response is a success
    # assert data.get("status_code") in (200, 201)
    # data = supabase.table('authority').select('accid').execute()
    # print(data)

    # bulk insert
    # data = supabase.table('cities').insert([
    # {'name': 'Gotham', 'country_id': 556 },


def get_national_officers():
    officers = supabase.table('authority').select(
        'accid, fname, lname').eq('level', 'national').execute()
    return list(officers)[0][1]