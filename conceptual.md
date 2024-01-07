### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?

  It is a structure database which store data in tables

- What is the difference between SQL and PostgreSQL?

  sql is the standard and the postgre implement that standard plus some additional functionality.

- In `psql`, how do you connect to a database?

​    by typing in psql with credentials and db name

- What is the difference between `HAVING` and `WHERE`?

  Where is used for conditional filtering for non-group by whereas having is for group by 

- What is the difference between an `INNER` and `OUTER` join?

  

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?

   Left join return all the rows that matching with left table while inner join return rows that matching in both table

- What is an ORM? What do they do?

  ORM map object to sql and vise versa

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?

   ajax is client side and needs to be same origin while requests is server side and doesn't need to be same origin
  
- What is CSRF? What is the purpose of the CSRF token?

  CSRF is like a a secret token that ensure the user from the UI is the one making the call instead of some random hacker

- What is the purpose of `form.hidden_tag()`?

   To hide the form that is used to generate CSRF token.
