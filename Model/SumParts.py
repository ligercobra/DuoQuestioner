#coding:utf-8
import re
import calendar
from Cookie import SimpleCookie
import time
import os
import sys
import urllib2
from dateutil.relativedelta import relativedelta
import datetime

#parts class
class SumParts(object):
    
    def __init__(self):
        pass

    #check_input year,month,day
    def check_ymd(self,year,month=None,day=None):
        if(day == None):
            day="1"
        if(month==None):
            month="1"
        if(not (isinstance(year,str) and year.isdigit() and 
            len(year)==4) and int(year) < 2100 and int(year) > 2000):
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
    
    def check_page(self,page):
        if(not (isinstance(page,str) and int(page) > 0 and int(page) <6 )):
            return False
        return True
    
    def count_char(self,u_str):
        n=0
        if(not isinstance(u_str,unicode)):
            return False
        for c in u_str:
            wide_chars = u"WFA"
            eaw = unicodedata.east_asian_width(c)
            if(wide_chars.find(eaw) > -1):
                n +=1
            return n

    def check_userauth(self,regid,passwd):
        if(re.match(r"^\w{4,30}$",regid) and re.match(r"^\w{6,30}$",passwd)):
            return True
        else:
            return False
    
    def check_id_pass(self,mregid,mupass):
        if(mregid.isalnum() and mupass.isalnum()):
            return True
        else:
            return False

    def check_id_seskey(self,mregid,mseskey):
        if(re.match(r"\w{4,30}",mregid) and re.match(r"(\w|\-){20,}",mseskey)):
            return True
        else:
            return False

class Transporter(object):

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
            print(self.ck.output(i))

    def set_ck(self,**kws):
        cktime = time.time() + 86400
        for i in kws:
            self.ck[i] = urllib2.quote(kws[i])
            self.ck[i]["expires"] = time.strftime('''
                                        %a, %d %b %Y 
                                        %H:%M:%S GMT''',
                                        time.gmtime(cktime))
            print(self.ck.output(i))
    
    def destroy_allck(self):
        for i in self.ck:
            self.ck[i] = "-1"
            self.ck[i]["expires"] = "Tue, 31-Dec-2001 00:00:00 GMT"
            print(self.ck.output(i))

    def reset_ck(self):
        cktime = time.time() + 86400
        for i in self.ck:
            self.ck[i]["expires"] = time.strftime('''
                                        %a, %d %b %Y 
                                        %H:%M:%S GMT''',
                                        time.gmtime(cktime))
            print(self.ck.output(i))

    def to_notfound(self):
        print("Content-type:text/html\n\n")
        print("Sorry, Not Found.<br />")
        print('''Return to <a href="./myhome.py">Home</a>,please.''')
        sys.exit()

    def to_proj_register(self):
        print("Location: myproject.py\n\n")

    def to_login_error(self):
        self.destroy_allck()
        self.set_ck(long_time="1")
        print("Location: login.py\n\n")
    
    def to_login_failed(self):
        self.destroy_allck()
        self.set_ck(login_e="1")
        print("Location: login.py\n\n")
    
    def to_profile_result(self):
        print("Location: myprofile.py\n\n")

    def to_rep_result(self,myear,mmonth,mday,mpid,fl):
        if(fl):
            self.set_ck(repreg="1")
        else:
            self.set_ck(repreg="0")
        ret_loc = "myhome.py?&pid=%d&year=%d&month=%d&day=%d"%(mpid,myear,mmonth,mday)
        print("Location: "+ret_loc+"\n\n")

    def to_registuser_result(self,fl):
        if(fl):
            self.set_ck(ureg="1")
        else:
            self.set_ck(ureg="0")
        print("Location: login.py\n\n")

    def to_myhome(self):
        print("Location: myhome.py\n\n")

    def to_prof_tlc_result(self,myear,mmonth,mday,fl):
        if(fl):
            self.set_ck(repreg="1")
        else:
            self.set_ck(repreg="0")
        ret_loc = "prof_myhome.py?year=%d&month=%d&day=%d"%(myear,mmonth,mday)
        print("Location: "+ret_loc+"\n\n")
