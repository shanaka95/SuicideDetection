import db_connect,google_api,re,thread
import numpy as np
import matplotlib.pyplot as plt
import random
import string
f=open('ignore.txt','a')
f.close()
def add_data(user,text):
  try:
    special=['i want to die','commit suicide','come to my funeral','suiciding']
    normal=['hello','hi','dude','hey']
    score,magnitude=google_api.get_values(text)
    for i in special:
        if i in text.lower():
            score=-1.0
            magnitude=20.0
    
    db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
    cur.execute('insert into user_records(user_name,text) values ("%s","%s")'%(user,text))
    db.commit()    
    if score<0 and text.strip() not in normal:
        words=text.split()
        cur.execute('select * from patterns')
        data=cur.fetchall()
        cur.execute('select keyword from keywords where user_name="%s"'%(user))
        data2=cur.fetchall()
        
        d1=map(lambda x:x[0],data)
        wordlist=d1+map(lambda x:x[0],data2)
        print 1
        exp = re.compile('|'.join(wordlist).lower())
        print 2
        if re.search(exp, text.lower()) or score<=-1:
            
            cur.execute('insert into user_experience(uname,score,magnitude) values ("%s","%s","%s")'%(user,str(score),str(magnitude)))
            cur.execute('update helpme.chat_messages values score="%s",magnitude"%s",measured=1 where id=%s'%(str(score),str(magnitude),str(msg_id)))            
            db.commit()
            thread.start_new_thread( user_keywords, (user,text, ) )
            thread.start_new_thread( pattern_change, (d1,text,magnitude, ) )
            
            return 'User has emotions related to suiciding!'
        else:
            cur.execute('insert into user_experience(uname,score,magnitude) values ("%s","%s","%s")'%(user,str(score),str(magnitude)))
            db.commit()
            return 'User has negative emotions'
        
    else:
        cur.execute('insert into user_experience(uname,score,magnitude) values ("%s","%s","%s")'%(user,str(score),str(magnitude)))
        db.commit()
        return 'User has positive emotions'
  except Exception as e:
      return e

    
def pattern_change(data,text,magnitude):
    for i in data:
        if i.lower() in text.lower():
            db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
            cur.execute('select magnitude from patterns where keyword="%s"' %(i.lower()))
            magnitude=(magnitude+float(cur.fetchone()[0]))/2
            cur.execute('update patterns set magnitude="%s",count=count+1 where keyword="%s"'%(str(magnitude),i.lower()))
            db.commit()
    
def user_keywords(user,text):
    db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
    words=text.split()
    f=open('ignore.txt','r')
    ignore_words=f.read().split(',')
    f.close()
    f=open('ignore.txt','a')
    for i in words:
        if '.' in i:
            new_i=i.split('.')
            i=new_i[0]
            words+=[new_i[1]]
        if i not in ignore_words:
            score,magnitude=google_api.get_values(i)
            if score>1.2:
                f.write(i+',')
            else:
                cur.execute('insert into keywords(user_name,keyword) values ("%s","%s")'%(user,i))
                db.commit() 
    f.close()
                    
def dead_user(user):
    db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
    cur.execute('select keyword from keywords where user_name="%s"'%(user))
    data=cur.fetchall()
    d=[]
    for i in data:
        if i[0] not in d:
            d+=[i[0]]
    l1,l2=[],[]
    for i in d:
        cur.execute('select count(keyword) from keywords where keyword="%s"'%(i))
        data=cur.fetchone()
        l1+=[i]
        l2+=[data[0]]
    print l1,l2
    m = 2
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    for j,i in enumerate(l2):
        if i not in list(set(data)-set(filtered)):
          try:
            cur.execute('insert into patterns(keyword,count,magnitude) values ("%s",0,0)'%(l1[j]))
            db.commit()
          except:
              pass
            
        
def get_graph(user):
  db,cur=db_connect.connect('Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh')
  cur.execute('select score,magnitude from user_experience where score<0 and uname="%s"'%(user))
  data = cur.fetchall()
  x=np.array(range(len(data)))
  y=map(lambda x:x[1], data)
  '''yy=[y[0]]
  for i in range(1,len(y)):
    yy+=[yy[i-1]+y[i]]
  print y,yy'''
  cur.execute('select score,magnitude from user_experience where score>0 and uname="%s"'%(user))
  data = cur.fetchall()
  x2=np.array(range(len(data)))
  y2=map(lambda x:x[1], data)

  fig = plt.figure(figsize=(15,8))
  ax1 = fig.add_subplot(111)
  
  ax1.plot(x, y, label='Negative Emotions', color='r', marker='o')
  ax1.plot(x2, y2, label='Positive Emotions', color='g', marker='o')

  plt.xticks(x)
  plt.xlabel('Chats')
  plt.yticks(x)
  plt.ylabel('Magnitude')
  handles, labels = ax1.get_legend_handles_labels()
  lgd = ax1.legend(handles, labels, loc='upper center', bbox_to_anchor=(1.15,1))
  ax1.grid('on')

  
  char_set = string.ascii_uppercase +string.ascii_lowercase+ string.digits
  fname=''.join(random.sample(char_set*6, 30))+'.png'
  plt.savefig(fname ,bbox_inches="tight")
  return fname

        
