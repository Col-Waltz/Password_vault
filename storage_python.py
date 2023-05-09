

Users={} #{'user_id': {'Service_name': ['login','password']}}

    
def new_user(user_id):
    if user_id not in Users:
        return True
    else:
        return False
        
def add_new_user(user_id):
    Users[user_id] = {}

def org_name_check(user_id,org_name):
    if org_name in Users.get(user_id):
        return True
    else:
        return False
    
def storage_empty(user_id):
    if len(Users[user_id]) == 0:
        return True
    else:
        return False
    
def push_data(user_id,data):
    Users[user_id].update({data['organization']:[data['login'],data['password']]})

def get_login(user_id,org_name):
    return Users.get(user_id).get(org_name)[0]

def get_password(user_id,org_name):
    return Users.get(user_id).get(org_name)[1]

def pop_data(user_id,data):
    Users[user_id].pop(data['organization'])

def get_all_orgs(user_id):
    return Users[user_id].keys()
