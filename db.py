import pymongo
 
connection = pymongo.MongoClient('localhost', 27017)
 
db = connection.ntrack

def init_db(db):
    if 'users' not in db.list_collection_names():
        db.create_collection('users')

def add_user(db, user_inform):
    if not len(list(db['users'].find({'id': user_inform['id']}))) == 0:
        return False
    db['users'].insert_one(user_inform)
    return True

def add_user_projects(db, user_id, project):
    user = db['users'].find_one({'id': user_id})
    if project in user['projects']:
        return False
    db['users'].update_one({'id': user_id}, {'$push': {'projects': project}})
    return True

def remove_user_projects(db, user_id, project):
    user = db['users'].find_one({'id': user_id})
    projects = user['projects'].remove(project)
    if projects is None:
        projects = []
    db['users'].update_one({'id': user_id}, {'$set': {'projects': projects}})

def load_user_inform(db, user_id):
    user = db['users'].find_one({'id': user_id})
    return user