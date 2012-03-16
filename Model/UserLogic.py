#-*- coding:utf-8 -*-

import peewee

MYDB = peewee.MySQLDatabase("duodb",
                            user="user",
                            host="localhost",
                            port=3306,
                            passwd="password")

class BaseModel(peewee.Model):
    class Meta:
        database = MYDB

class AnsTB(BaseModel):
    ansid = peewee.PrimaryKeyField() #primary key index
    usid = peewee.IntegerField() #user id
    qid = peewee.IntegerField() #question id
    secid = peewee.IntergerField() #section id
    anstime = peewee.DateTimeField() #time of answer
    ans = peewee.IntergerField() #user's answer(1 or 0)

class LastTB(BaseModel):
    lid = peewee.PrimaryKeyField() #primary key index
    usid = peewee.IntegerField() #user id
    qid = peewee.IntegerField() #question id
    secid = peewee.IngerField() #section id
    anstime = peewee.DateTimeField() #time of answer
    ans = peewee.IntegerField() #user's answer(1 or 0)

class QuesTB(BaseModel):
    qid = peewee.PrimaryKeyField() #quesiton id,primary key index
    en = peewee.TextField() #duo english text
    jp = peewee.TextField() #duo japanese text
    secid = peewee.IntegerField() #section id

class SecNum(BaseModel):
    secid = peewee.PrimaryKeyField() #section id
    qnum = peewee.PrimaryKeyField() #section's qustion number

class UserLogic(object):
    def __init__(self):
        AnsTB.create_table(True)
        LastTB.create_table(True)
        QuesTB.create_table(True)
        SecNum.create_table(True)

class UserSelect(UserLogic):
    
    def last_by_section(self,usid,secid,anstime=None,ans=None):
        for i in secid:

        sq = LastTB.select().where( 

