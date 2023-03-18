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
    user = db['users'].find({'id': user_id})
    user['projects'].append(project)

