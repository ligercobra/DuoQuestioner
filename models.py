#coding: utf-8

import os
import hashlib
import peewee
import uuid
import ConfigParser
import csv
from datetime import datetime

#mysqlconf = ConfigParser.SafeConfigParser()
#mysqlconf.read("../mysqlconf.ini")
#MYDB = peewee.MySQLDatabase(mysqlconf.get('mysql','dbname'),
#                            user=mysqlconf.get('mysql','user'),
#                            host=mysqlconf.get('mysql','host'),
#                            port=int(mysqlconf.get('mysql','port')),
#                            passwd=mysqlconf.get('mysql','passwd')
#                            )
MYDB = peewee.SqliteDatabase('DuoDB.db')
csvfile = '../duo_table.csv'

class BaseModel(peewee.Model):
    class Meta:
        database = MYDB

#define userauth table
class UserAuth(BaseModel):
    usid = peewee.PrimaryKeyField()
    regid = peewee.CharField(unique=True)
    upass = peewee.CharField()
    uname = peewee.CharField(null=True)
    seskey = peewee.TextField(null=True)

class AnsTB(BaseModel):
    ansid = peewee.PrimaryKeyField() #primary key index
    usid = peewee.IntegerField() #user id
    qid = peewee.IntegerField() #question id
    secid = peewee.IntegerField() #section id
    anstime = peewee.DateTimeField() #time of answer
    ans = peewee.IntegerField() #user's answer(1 or 0)

class LastTB(BaseModel):
    lid = peewee.PrimaryKeyField() #primary key index
    usid = peewee.IntegerField() #user id
    secid = peewee.IntegerField() #section id
    ansdate = peewee.DateTimeField(null=True) #answer rate last time

class QuesTB(BaseModel):
    qid = peewee.PrimaryKeyField() #quesiton id,primary key index
    en = peewee.TextField() #duo english text
    jp = peewee.TextField() #duo japanese text
    secid = peewee.IntegerField() #section id

class SecNum(BaseModel):
    secid = peewee.PrimaryKeyField() #section id
    qnum = peewee.IntegerField() #section's qustion number

#base class
class UserBase(object):
    def __init__(self):
        #make user table
        UserAuth.create_table(True) 
        AnsTB.create_table(True)
        LastTB.create_table(True)
        QuesTB.create_table(True)
        SecNum.create_table(True)

    def update_ses(self,mregid):
        mseskey = str(uuid.uuid4())
        sq = peewee.UpdateQuery(UserAuth,seskey=mseskey).where(regid=mregid)
        sq.execute()
        return mseskey

class UserLogin(UserBase):

    def _check_collation(self,mregid,mpasswd):
        sq = UserAuth.select().where(regid=mregid)
        origin_p = [u.upass for u in sq]
        #length=0 is not found regid or not match regid and upass
        if(len(origin_p) == 0 or origin_p[0] != hashlib.sha224(mpasswd).hexdigest()):
            return False

        if(origin_p[0] == hashlib.sha224(mpasswd).hexdigest()):
            return True
    
    def login(self,mregid,mpasswd):
        if(self._check_collation(mregid,mpasswd)):
            return(super(UserLogin,self).update_ses(mregid))
        return False

class UserRegist(UserBase):

    #found duplicated regid = False, else = True
    def _check_duplication(self,mregid):
        sq=UserAuth.select().where(regid=mregid)
        if(sq.where().exists()):
            return False
        return True
    
    def userinsert(self,mregid,mpasswd):
        if(self._check_duplication(mregid)):
            mp = hashlib.sha224(mpasswd).hexdigest()
            iq = peewee.InsertQuery(UserAuth,regid=mregid,upass=mp)
            iq.execute()
            return True
        else:
            return False

class UserInfo(UserBase):
    
    def get_uinfo(self,mregid,mseskey):
        sq = UserAuth.select().where(seskey=mseskey)
        if(not sq.where(regid=mregid).exists()):
            return False
        sq = UserAuth.select().where(regid=mregid)
        sq.execute()
        uinfo = [u for u in sq]
        baseinfo = {"usid":uinfo[0].usid,
                    "regid":uinfo[0].regid,
                    "uname":u"No Name",
                    "seskey":uinfo[0].seskey
                    }
        if(uinfo[0].uname!=None):
            baseinfo["uname"] = uinfo[0].uname
        return baseinfo
    
    def add_uname_resfield(self,musid,muname):
        iq = peewee.UpdateQuery(UserAuth,uname=muname).where(
                usid=musid)
        iq.execute()
        return True
    
    def prof_all_usid_uname(self):
        sq = UserAuth.select(['usid','uname'])
        sq.execute()
        all_usid = [{"usid":u.usid, "uname":u.uname} for u in sq]
        return all_usid

class UserSelect(UserBase):
    
    def last_by_section(self,usid,secid):
        sq = LastTB.select().where(usid=usid,secid__in=secid)
        tmp_res = [{"usid":usid,"secid":k,"ansrate":None} for k in secid]
        res = [v for v in sq]
        return res

    def secnum_by_section(self,secid):
        sq = SecNum.select().where(secid__in=secid)
        res = [{"qnum":u.qnum,"secid":u.secid} for u in sq]
        return res

    def section_question(self,secid):
        sq = QuesTB.select().where(secid__in=secid)
        res = [{"qid":u.qid, "en":u.en, "jp":u.jp} for u in sq]
        return res
 
    def get_qid(self,secid):
        sq = QuesTB.select().where(secid__in=secid)
        res = [{"qid":u.qid} for u in sq]
        return res
 
class UserInsert(UserBase):
    def questb_all(self):
        reader = csv.reader(open(csvfile, 'rU'), dialect='excel')
        for row in reader:
            u_en = unicode(row[1],'utf-8')
            u_jp = row[2].rsplit('.')[1]
            u_jp = unicode(u_jp,'utf-8')
            u_secid = int(unicode(row[3],'utf-8'))
            iq = peewee.InsertQuery(QuesTB, en=u_en, jp=u_jp, secid=u_secid)
            iq.execute()

    def result(self, usid, secid, qid_ans):
        nowtime = datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
        for dict_qa in qid_ans:
            iq = AnsTB.insert(usid=usid, secid=secid, \
                qid=dict_qa['qid'], ans=dict_qa['ans'], \
                anstime=nowtime)
            #iq = peewee.InsertQuery(AnsTB, usid=usid, secid=secid, \
            #    qid=dict_qa['qid'], ans=dict_qa['ans'], \
            #    anstime=nowtime)
            iq.execute()
