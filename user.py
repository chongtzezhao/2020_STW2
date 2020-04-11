'''
from app import mysql, app

def check_user_password(userid, password):
    with app.app_context():  # needed for mysql to be valid, else mysql.connection = None
        cur = mysql.connection.cursor()
        user_exists = cur.execute('SELECT Password FROM User WHERE UserID = "%s"' % (userid))
        if user_exists:
            correct_password = cur.fetchone()[0]
            if password == correct_password:
                return 1
            else:
                return 0
        else:
            return -1

def get_name(userid):
    with app.app_context():  # needed for mysql to be valid, else mysql.connection = None
        cur = mysql.connection.cursor()
        user_exists = cur.execute('SELECT Name FROM User WHERE UserID = "%s"' % (userid))
        if user_exists:
            name = cur.fetchone()[0]
            return name
        
def create_user(userid, user_name, password):
    with app.app_context():  # needed for mysql to be valid, else mysql.connection = None
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO User (UserID, Name, Password) VALUES("%s", "%s", "%s")'
            % (userid, user_name, password))
        mysql.connection.commit()
        cur.close()
'''
from app import User, db
from hash_algo import hash_password, verify_password

def check_user_password(userid, password):
    try:
        user = User.query.filter_by(UserID=userid).first()
    except:
        user = User.query.filter_by(UserID=userid).first()
    if user:
        if verify_password(user.Password, password):
            return 1
        else:
            return 0
    else:
        return -1


def get_name(userid):
    try:
        user = User.query.filter_by(UserID=userid).first()
    except:
        user = User.query.filter_by(UserID=userid).first()
    if user:
        return user.Name
    else:
        return None


def create_user(userid, user_name, password, email):
    hashed_password = hash_password(password)
    new_user = User(userid, user_name, hashed_password, email)
    try:
        db.session.add(new_user)
    except:
        db.session.add(new_user)
    
    try:
        db.session.commit()
    except:
        db.session.commit()



if __name__ == "__main__":
    print(check_user_password('thepoppycat', 'qwerty'))
    #print(get_name('thepoppycat'))
