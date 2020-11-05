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
* Oppend s3 -> created a new bucket and added the appropriate user's groups and security policies for it.
which will host my static and media files after deployment to heroku

2. To connect django with the aws bucket:
* pip3 install boto3
* pip3 install django-storages
* pip3 freeze >requirements.txt
* settings.py : added django-storages to installed apps
* settings.py: added an if statment to check if on heroku, it should use the aws bucket in which i provided the bucket settings details
* disabled collect static: since now i have the aws bucket policy setup: django will collectstatic files automatically and upload them to s3.
* Created a custom storage classs using s3boto3 storage class from django storages : to tell django that in production
 use s3 to store  static files whenever someone runs collectstatic or uploads any image. and the location it should save both the static and media files

#### Project Cloning :
* Click to view the project env samples [.env.sample](https://github.com/Teemamin/spice_ur_look/blob/master/.env).
Should anyone be intrested in making future enhancements / work further on this project, you can clone as follows:
* At the top of my repo : click on the "code" button, which will present you with the following options :
1. Clone with HTTPS or an SSH key: [Generating a new key](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
* SSH key: click use SSH key : don't have any public SSH keys in your GitHub account, You can add a new public key,by clicking on the github provided link or try cloning this repository via HTTPS
* HTTPS : click on the copy icon on the right, which will copy the link on your clipbord
2. Open your Terminal : ensure that your current working directory is the location you want the clone directory to be in
3. git clone : paste in the HTTPS url you copied
4. ensure to check the requirements.txt for all the necessary dependencies you will need to install for the project
5. for further info on github cloning : [Github](https://docs.github.com/en/enterprise/2.13/user/articles/cloning-a-repository).






