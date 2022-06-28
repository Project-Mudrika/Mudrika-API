import os
from supabase import create_client, Client

from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def insert_into_db(acid, level, fnam, lnam, sta, dis, user):
    data = supabase.table('authority').insert(
        {'accid': acid, 'level': level, 'fname': fnam, 'lname': lnam, 'state': sta, 'district': dis, 'username': user}).execute()
    return data


def fetch_all_data():
    data = supabase.table('authority').select(
        'accid', 'level', 'fname', 'lname', 'state', 'district', 'username').execute()
    print(data)
    print('\n')

    # insert_into_db("1009", "national", "Devu", "diya", "kerala", "tvm", "devudiya")
    # fetch_all_data()

    #data = supabase.table('authority').select('accid').execute()
    # print(data)
    #data = supabase.table('authority').insert({'accid': '1335', 'fname': "aarya" }).execute()
    # assert if insert response is a success
    #assert data.get("status_code") in (200, 201)
    #data = supabase.table('authority').select('accid').execute()
    # print(data)

    # bulk insert
    # data = supabase.table('cities').insert([
    #{'name': 'Gotham', 'country_id': 556 },
