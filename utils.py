# -*- coding:utf-8 -*-

import os
import sys
import time
import re
import urllib2
from dateutil.relativedelta import relativedelta
import datetime
import ConfigParser
from Cookie import SimpleCookie

http_header = "Content-Type:text/html; charset=utf-8; "

class ManageCookie(object):

    def __init__(self): 
        self.ck = SimpleCookie()
        self.ck.load(os.environ.get("HTTP_COOKIE",""))
    
    def assemble_ck2dict(self):
        d = {}
        for i in self.ck:
            d[i] = self.ck[i].value
        return d

    def destroy_ck(self,*args):
        for i in args:
            if(i in self.ck):
                self.ck[i]["expires"] = "Tue, 31-Dec-2001 00:00:00 GMT"

    def destroy_allck(self):
        for i in self.ck:
            self.ck[i] = "-1"
            self.ck[i]["expires"] = "Tue, 31-Dec-2001 00:00:00 GMT"

    def set_ck(self,**kws):
        cktime = time.time() + 86400
        for i in kws:
            self.ck[i] = urllib2.quote(kws[i])
            self.ck[i]["expires"] = time.strftime('''
                                        %a, %d %b %Y 
                                        %H:%M:%S GMT''',
                                        time.gmtime(cktime))

    def reset_ck(self):
        cktime = time.time() + 86400
        for i in self.ck:
            self.ck[i]["expires"] = time.strftime('''
                                        %a, %d %b %Y 
                                        %H:%M:%S GMT''',
                                        time.gmtime(cktime))

    def check_ses_reg(self):
        if(not ("regid" in self.ck) or not ("seskey" in self.ck)):
            return False,None
        else:
            tmp_ses = self.ck["seskey"].value
            tmp_reg = self.ck["regid"].value
            if(not check_id_seskey(mregid=tmp_reg,mseskey=tmp_ses)):
                return False,None
            else:
                return tmp_ses,tmp_reg

    def print_ck(self):
        for i in self.ck:
            print(self.ck.output(i))

#the following the utils function

def to_stand_res():
    print(http_header)

def to_notfound():
    print(http_header)
    print("Sorry, Not Found.<br />")
    print('''Return to <a href="./home.py">Home</a>,please.''')
    sys.exit()

def to_proj_register():
    print("Location: home.py\n\n")
    sys.exit()

def to_login():
    print("Location: login.py\n\n")
    sys.exit()

def to_home():
    print("Location: home.py\n\n")
    sys.exit()

#check_input year,month,day
def check_ymd(year,month=None,day=None):
    if(day == None):
        day="1"
    if(month==None):
        month="1"
    if(not (isinstance(year,str) and year.isdigit() and 
        len(year)==4 and int(year) < 2100 and int(year) > 2000)):
        return False
    if(not (isinstance(month,str) and month.isdigit() and 
        len(month) < 3 and int(month) > 0 and int(month) < 13)):
        return False
    if(not (isinstance(day,str) and day.isdigit() and 
        len(day) < 3 and int(day) > 0 and int(day) < 32)):
        return False
    '''
        指定された月の最後の日
    '''
    lstday = datetime.date(int(year),int(month),1) + relativedelta(day=31)
    if(lstday.day >= day):
        return False
    return True

def check_userauth(regid,passwd):
    if(re.match(r"^\w{4,30}$",regid) and re.match(r"^\w{6,30}$",passwd)):
        return True
    else:
        return False

def check_id_pass(mregid,mupass):
    if(mregid.isalnum() and mupass.isalnum()):
        return True
    else:
        return False

def check_id_seskey(mregid,mseskey):
    if(re.match(r"\w{4,30}",mregid) and re.match(r"(\w|\-){20,}",mseskey)):
        return True
    else:
        return False

#form has year, month, day?
def date_ref(mform):
    nw = datetime.datetime.today()
    if(("year" in mform) and ("month" in mform) and ("day" in mform)):
        tmp_y = mform.getfirst("year","")
        tmp_m = mform.getfirst("month","")
        tmp_d = mform.getfirst("day","")
        if(check_ymd(year=tmp_y,month=tmp_m,day=tmp_d)):
            return int(tmp_y),int(tmp_m),int(tmp_d)
        else:
            return nw.year,nw.month,nw.day
    else:
        return nw.year,nw.month,nw.day

