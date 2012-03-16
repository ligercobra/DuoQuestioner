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
    ansid = peewee.PrimaryKeyField()
    usid = peewee.IntegerField()
    secid = peewee.IntergerField()
    anstime = peewee.DateTimeField()
    ans = peewee.IntergerField()

class LastTB(BaseModel):
    lansid = peewee.PrimaryKeyField()
    usid = peewee.IntegerField()
    secid = peewee.IngerField()
    anstime = peewee.DateTimeField()
    ans = peewee.IntegerField()

class QuesTB(BaseModel):
    qid = peewee.PrimaryKeyField()
    secid = peewee.IntegerField()
    en = peewee.TextField()
    jp = peewee.TextField()

class UserLogic(object):
    def __init__(self):
        AnsTB.create_table(True)
        LastTB.create_table(True)
        QuesTB.create_table(True)

