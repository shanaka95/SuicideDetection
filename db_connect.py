import MySQLdb
def connect(auth_key):
    db = MySQLdb.connect(host="localhost",user="root",passwd="",db="ihack")
    cur = db.cursor()
    cur.execute('select auth_key from auth where app_name="db_connect"')
    if cur.fetchone()[0]==auth_key:
        return db,cur
    else:
        return 'Authenticaion Failed!'
