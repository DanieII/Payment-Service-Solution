# Welcome to our Payment Service Solution
This is a web app built in less than 48 hours as a part of the [SoftUni Software Fest 2023](https://fest.softuni.bg/softuni-fest-2023-software/)<br>
It offers business and customer types of accounts:  
Business part allows sellers to publish offers and services  
Customer part shows all the active offers, allows search by business name or part of it and payment with Stripe and Coinbase.
There are also some statistics that business part shows to its users.
The app is entirely writen in Django framework. It has responsive design and uses PostgreSQL as a database. 
It can be easily switched to any of these too:/
Officially supported: MariaDB, MySQL, Oracle, SQLite/
3rd party: CockroachDB, Firebird, Google Cloud Spanner, Microsoft SQL Server, Snowflake, TiDB, YugabyteDB

### Customer home page screenshots:
![Screenshot 2023-11-01 at 15 39 50](https://github.com/DanieII/Payment-Service-Solution/assets/110739078/dbcedae4-ebe9-46e6-aba3-bf1dac9c78e9)
![Screenshot 2023-11-01 at 15 39 57](https://github.com/DanieII/Payment-Service-Solution/assets/110739078/edda9fae-ef57-4934-8db5-cda3622d244a)

### Things that you need in order to test the payment systems:
- For Stripe you can use one of the 3 provided test cards:
 1. 4000000000009995 - Failed payment
 2. 4000002500003155 - Requires authentication (3D)
 3. 4242424242424242 - Successful payment
 (use date in the future like 12/34
 any 3 numbers as CVC)
![image](stripe.jpg)


- For Coinbase (there is no sandbox there) you need real crypto in order to make
successful payment.
![image](coinbase.jpg)

#### Messages that consumer will see on successful or failed(cancelled) payment:
![image](failed.jpg)


If you want to build the app you need to have StripeCli:  
https://stripe.com/docs/stripe-cli  
stripe login (for loging into your Stripe account)  
stripe listen --forward-to localhost:8000/webhooks/stripe/ (to get webhook key and to listen for successful or not payments)  
Also you will need Stripe publishable and secret keys and Coinbase API in order to get real and successful payments.  

Hope you'll enjoy it!
