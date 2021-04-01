import psycopg2
from telebot import types
from telebot.util import is_pil_image


host = "ec2-52-45-73-150.compute-1.amazonaws.com"
port = 5432
user = "tbpsgtuwiktyle"
password = "990c6b764260c7df82deabb2729743edee7ee35dbf42fe29487ee8733c6c8e16"
database = "dnn08v7n3gd0o"

# postgres://tbpsgtuwiktyle:990c6b764260c7df82deabb2729743edee7ee35dbf42fe29487ee8733c6c8e16@ec2-52-45-73-150.compute-1.amazonaws.com:5432/dnn08v7n3gd0o

class PostgresDB:
    def addUser(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"insert into users(tg_id) values ({tg_id})")
        conn.commit()
        conn.close()
    def getuser(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"select * from users where tg_id = {tg_id}")
        for i in cursor:
            return i
    def vqdbishadd(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"insert into vqtdb (tg_id) values ({tg_id})")
        conn.commit()
        conn.close()
    def vqdbsotuvadd(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"insert into vqtsotuv (tg_id) values ({tg_id})")
        conn.commit()
        conn.close()
    def vqdbishCLear(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"delete from vqtdb where tg_id= {tg_id}")
        conn.commit()
        conn.close()
    def vqdbSotuvCLear(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"delete from vqtsotuv where tg_id= {tg_id}")
        conn.commit()
        conn.close()
    def GetTypeSotuv(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"select type from vqtsotuv where tg_id={tg_id}")
        for i in cursor:
            if (type(i)==tuple):
                return i
        return ('Hechnima',)
    def vqdbIshSetLastMessage(self,tg_id,text):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"update vqtdb set lastmessage='{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def vqdbSotuvSetLastMessage(self,tg_id,text):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"update vqtsotuv set lastmessage='{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def EnterTypeIsh(self,tg_id,text):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"update vqtdb set type= '{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def EnterTypeSotuv(self,tg_id,text):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"update vqtsotuv set type = '{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def EnterUserNameIsh(self,tg_id,text):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"update vqtdb set username= '{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def EnterUserNameSotuv(self,tg_id,text):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"update vqtsotuv set username = '{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def GetLastMessageSotuv(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"select lastmessage from vqtsotuv where tg_id={tg_id}")
        for i in cursor:
            return i
        return ('Hechnima',)
    def altertablesotuv(self,tg_id,text):
        last_m=self.GetLastMessageSotuv(tg_id)[0]
        text=text.replace("'","@!")
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"update  vqtsotuv set {last_m} = '{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def GetLastMessageIsh(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"select lastmessage from vqtdb where tg_id={tg_id}")
        for i in cursor:
            return i
        return ('Hechnima',)
    def altertableish(self,tg_id,text):
        last_m=self.GetLastMessageIsh(tg_id)[0]
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        text=text.replace("'","@!")
        cursor.execute(f"update vqtdb set {last_m} = '{text}' where tg_id={tg_id}")
        conn.commit()
        conn.close()
    def ReadyIshPost(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"select *from vqtdb where tg_id = {tg_id}")
        for i in cursor:
            r=i
        result={'full_name':r[1],'yosh':r[2],'ishturi':r[3],'pathphoto':r[4],'username':r[5],'tel':r[6],'hudud':r[7]
        ,'narxi':r[8],'vaqt':r[9],'qoshimcha':r[10],'type':r[12]
        }
        return result
    def ReadySotuvPost(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"select * from vqtsotuv where tg_id = {tg_id}")
        for i in cursor:
            R=i
        result={'full_name':R[2],'tovar':R[3],'photo_path':R[4],'tel':R[5],'manzil':R[6],'narx':R[7],
        'qoshimcha':R[8],'type':R[9],'username':R[11]}
        return result
    def SaveArchieveIsh(self,tg_id,full_name,yosh,ishturi,pathphoto,username,tel,hudud,narxi,vaqt,qoshimcha,type):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"insert into archiveworkpost (tg_id,full_name,yosh,ishturi,pathphoto,username,tel,hudud,narxi,vaqt,qoshimcha,type) values ({tg_id},'{full_name}','{yosh}','{ishturi}','{pathphoto}','{username}','{tel}','{hudud}','{narxi}','{vaqt}','{qoshimcha}','{type}')")
        conn.commit()
        conn.close()  
    def SaveArchieveSotuv(self,tg_id,full_name,tovar,tel,manzil,narx,qoshimcha,type,username):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"insert into archivesotuv (tg_id,full_name,tovar,tel,manzil,narx,qoshimcha,type,username) values ({tg_id},'{full_name}','{tovar}','{tel}','{manzil}','{narx}','{qoshimcha}','{type}','{username}')")
        conn.commit()
        conn.close()
    def ClearArchievIsh(self,tg_id):
        conn=psycopg2.connect(database="ElonBot", user="postgres", password="inshaallah", host="localhost",port='5432')
        cursor=conn.cursor()
        cursor.execute(f"delete from archiveworkpost where tg_id={tg_id}")
        conn.commit()
        conn.close()
