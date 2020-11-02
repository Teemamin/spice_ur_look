## Deploying to Heroku:
----
 Creating heroku app and linking to github repo:
1. On Heroku website [click here](https://dashboard.heroku.com/) I logged into my heroku dashboard :
2. Clicked on create new app: gave the app a name and chose a region
3. On Heroku ->resources->add-ons->searched for Postgres database and provisioned the free version for my heroku app
4. To use Postgres back in gitpod: i installed dj_database_url, and psycopg2. with pip3 install dj_database_url
And pip3 install psycopg2-binary
5. Gitpod terminal: pip3 freeze --local > requirements.txt: which installed all the necessary dependencies for the project
6. Setting up Postgres database on gitpod: 
* settings.py: import dj_database_url
* At the databases setting: I temporarily commented out the default configuration, and replaced it with a call to dj_database_url.parse()
 and give it the Postgres database URL from Heroku.
* Ran "python3 manage.py showmigrations" on gitpod terminal to show all the migration
* Ran "python3 manage.py migrate" to apply all those migrations and get my database all set up.
7. Importing all products data to the new setup database:
* At the databases setting:  commented out the call to dj_database_url and switched back to the django default database
 "django.db.backends.sqlite3"
* Ran the following commands at gitpod terminal to create fixtures: 
python3 manage.py dumpdata products.Category --indent 4 > products/fixtures/category.json
python3 manage.py dumpdata products.Product --indent 4 > products/fixtures/products.json
8. Loading data to Postgres database: After the fixtures was created, i switched back to use dj_database_url database:
* on gitpod terminal: python3 manage.py load data categories
python3 manage.py load data products
9. setting-up superuser on Postgres: 
* on gitpod terminal: "python3 manage.py create superuser" entered the necessary requirements
10. Settings.py : now that i have both my databases setup:
* I added an if statment to check if on Heroku use Postgres database(using env variable) and if on gitpod use django.db.backends.sqlite3
11. Gitpod terminal: installed unicorn which will act as my webserver "pip3 install gunicorn"
* pip3 freeze --local > requirements.txt
* Created Procfile : To tell Heroku to create a web dyno.Which will run unicorn and serve the django app.
* temporarily disable collectstatic "heroku config: set Disable collectstatic=1" : so that heroku doesn't try collecting
static files.
12. Settings.py : added heroku app name to allowed hosts
* in my gitpod work environment CLI: $ heroku login : to login to heroku from my terminal
13. Gipod terminal: git add .
14. Gipod terminal: git commit -m "add all the changes"
15. Gipod terminal: git push -u heroku master

#### Creating and setting up AWS:

1. logged into my aws console: 
* Oppend s3 -> create a new bucket , gave the bucket a name,unchecked block all public access.
And acknowledged that the bucket will be public  and clicked create bucket
2. properties tab I turned on static website hosting and click save 
3. permissions tab:
* Added coors configuration:
which is going to set up the required access between my Heroku app and this s3 bucket.
* bucket policy tab select, policy generator :
-  policy type -> s3 bucket policy
- principals -> *
-  action -> get object
- ARN 
- lastly click add statement and generate policy
- copy the policy into the bucket policy editor.


