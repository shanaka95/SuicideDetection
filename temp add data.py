import db_connect
db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
f=open('a.txt','r').read()
for i in f.strip().split(','):
    i=i.replace(" ", "")
    try:
        cur.execute('insert into patterns (keyword,count,magnitude) values ("%s",0,0)'%(i.lower()))
    except Exception as e:
        print e
db.commit()
cur.close()
