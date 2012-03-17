#coding: utf-8

import os
import hashlib
import peewee
import uuid
import ConfigParser


mysqlconf = ConfigParser.SafeConfigParser()
mysqlconf.read("../mysqlconf.ini")
MYDB = peewee.MySQLDatabase(mysqlconf.get('mysql','dbname'),
                            user=mysqlconf.get('mysql','user'),
                            host=mysqlconf.get('mysql','host'),
                            port=int(mysqlconf.get('mysql','port')),
                            passwd=mysqlconf.get('mysql','passwd')
                            )
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

#base class
class UserBase(object):
    def __init__(self):
        #make user table
        UserAuth.create_table(True)
    
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

