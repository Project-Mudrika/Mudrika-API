import os
from supabase import create_client, Client
url: str = os.environ.get("https://netlauydpmmztazzzldy.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5ldGxhdXlkcG1tenRhenp6bGR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTUyODE4MTgsImV4cCI6MTk3MDg1NzgxOH0.EOi8V57Djyl7qSUwPHtrjvUn18keF2gVMeRkwnOB1cQ")
supabase: Client = create_client("https://netlauydpmmztazzzldy.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5ldGxhdXlkcG1tenRhenp6bGR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTUyODE4MTgsImV4cCI6MTk3MDg1NzgxOH0.EOi8V57Djyl7qSUwPHtrjvUn18keF2gVMeRkwnOB1cQ")

def insert_into_db(acid,level,fnam,lnam,sta,dis,user):
    data = supabase.table('authority').insert({'accid': acid,'level' : level, 'fname': fnam ,'lname' :lnam ,'state' : sta , 'district' : dis , 'username' : user}).execute()
    return data

def fetch_data():
    data = supabase.table('authority').select('accid','level','fname','lname','state','district','username').execute()
    print(data)
    print('\n')

insert_into_db("1009","national","Devu","diya","kerala","tvm","devudiya")
fetch_data()



#data = supabase.table('authority').select('accid').execute()
#print(data)
#data = supabase.table('authority').insert({'accid': '1335', 'fname': "aarya" }).execute()
# assert if insert response is a success
#assert data.get("status_code") in (200, 201)
#data = supabase.table('authority').select('accid').execute()
#print(data)

# bulk insert 
#data = supabase.table('cities').insert([
#{'name': 'Gotham', 'country_id': 556 },