import db_connect
def add_user(user_name,notes):
    db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
    cur.execute('insert into users(user_name,notes) values ("%s","%s")'%(user_name,notes))
    db.commit()
    cur.close()

def add_pattern(keyword,magnitude):
    db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
    cur.execute('select magnitude from patterns where keyword="%s"'%(keyword))
    data=cur.fetchone()
    if len(data)<1:
        cur.execute('insert into patterns(keyword,count,magnitude) values ("%s",1,"%s")'%(keyword,magnitude))
        db.commit()
        cur.close()
    else:
        cur.execute('update patterns set count=count+1 , magitude="%s" where keyword="%s"'%((magnitude+float(data[0]))/2,keyword))
        db.commit()
        cur.close()

def add_user_keyword(user,keyword):
    db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
    cur.execute('select magnitude from patterns where keyword="%s"'%(keyword))
    data=cur.fetchone()
    if data and len(data)<1:
        cur.execute('insert into patterns(keyword,count,magnitude) values ("%s",1,50.0)'%(keyword))
        cur.execute('insert into keywords(keyword,user_name) values ("%s","%s")'%(keyword,user))
        db.commit()
        cur.close()
    else:
        cur.execute('insert into keywords(keyword,user_name) values ("%s","%s")'%(keyword,user))
        db.commit()
        cur.close()    

