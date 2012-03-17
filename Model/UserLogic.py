#-*- coding:utf-8 -*-

import peewee
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
    ansrate = peewee.DateTimeField(null=True) #answer rate last time

class QuesTB(BaseModel):
    qid = peewee.PrimaryKeyField() #quesiton id,primary key index
    en = peewee.TextField() #duo english text
    jp = peewee.TextField() #duo japanese text
    secid = peewee.IntegerField() #section id

class SecNum(BaseModel):
    secid = peewee.PrimaryKeyField() #section id
    qnum = peewee.IntegerField() #section's qustion number

class UserLogic(object):
    def __init__(self):
        AnsTB.create_table(True)
        LastTB.create_table(True)
        QuesTB.create_table(True)
        SecNum.create_table(True)

class UserSelect(UserLogic):
    
    def last_by_section(self,usid,secid):
        sq = LastTB.select().where(usid=usid,secid__in=secid)
        res = [
                {"usid":u.qid,"qid":u.secid,"anstime":u.anstime,"ans":u.ans}
                for u in sq
                ]
        return res

    def secnum_by_section(self,secid):
        sq = SecNum.select().where(secid__in=secid)
        res = [{"qnum":u.qnum,"secid":u.secid} for u in sq]
        return res

