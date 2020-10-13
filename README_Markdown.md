This is a simple implementation of flask api with JWT(JSON WEB TOKENS). You get a token by logging in and send this token in headers for accessing every other routes.


# Table of Contents

1.  [Usage](#orgb732884)
    1.  [Login and get a token](#org9832bea)
    2.  [Creating a user](#orgd24b96a)
    3.  [Viewing user info](#org8f5dee1)
    4.  [Promoting a user](#orgf794b60)
    5.  [Deleting a user](#orgc4379ee)
    6.  [Creating a post](#org199daa1)
    7.  [Viewing post](#orgc436b68)
    8.  [Updating a post](#org35efcf3)
    9.  [Deleting a post](#org392f3b0)
2.  [Configuration](#orga9733d7)
    1.  [Installing dependencies](#orgc59a945)
    2.  [Database config](#org9c22f5a)
    3.  [Database initialization and migration](#org2dbc4d5)
    4.  [Setting up migration for existing database](#org8cf28e5)
    5.  [Creating an admin user](#orgfca0e17)
3.  [Application registration tokens](#org80ec986)
4.  [Loosening other routes](#orgfc6484c)
5.  [TODOS](#orgece8575)


<a id="orgb732884"></a>

# Usage

This api has user and post tables in db. Every routes relating to &rsquo;user&rsquo; and &rsquo;post&rsquo; requires a token in the header which can be obtained by logging in throgh login route.

This assumes you have completed the configuration, created admin user and have its credentials. [See configuration section](#orga9733d7).

NOTE: Any illegal or failed requests on any route will generate non-200 status code and return a json dict with one &ldquo;message&rdquo; key stating the reason

Example:

    {"message": "no user found"}


<a id="org9832bea"></a>

## Login and get a token

ENDPOINT: &ldquo;login&rdquo; [GET REQ]
Payload: auth(username, pass)

    import requests
    from requests.auth import HTTPBasicAuth
    
    URL = "https://apiurl.com"
    # fill username and password with your acc info
    auth = HTTPBasicAuth("username", "password")
    
    login_response = requests.get(URL+"/login", auth=auth)
    login_response.status_code # confirm that its 200
    
    token = login_response.json()["token"]
    
    headers = {
        "x-access-token": token
    }

RESPONSE: 200

    {"token": "soasloiwurpoewiurpowierupwoeirf"}

For accessing every other route, you need to specify this token in the header as value of &ldquo;x-access-token&rdquo;.

NOTE: This token has no time limit and will never expire, [see why.](#org80ec986) For making expirable tokens have a look at [here](https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp).


<a id="orgd24b96a"></a>

## Creating a user

ENDPOINT: &ldquo;user&rdquo; [POST REQ]
REQ: admin token

Creating a user requires admin account&ldquo;s token. You send a post request to the &rdquo;user&ldquo; endpoint.

The payload should have username and password.

    headers = {"x-access-token": token}
    data = {"username": "some usename", "password": "my password"}
    
    create_user = requests.post(URL+"/user", data=data, headers=headers

Response: 200

    {
        "message": "User created successfully"
    }


<a id="org8f5dee1"></a>

## Viewing user info

ENDPOINT: &ldquo;user&rdquo; [GET REQ]
REQ: admin token

Sending the request gets you all users info

    headers = {"x-access-token": token}
    requests.get(URL+"/user", headers=headers)

RESPONSE: 200

    {"users": [
        {"admin": true, "id": 1,
         "password": "sha256$Sot2tcp9$671301dae8s45ad6f2fe0f583f8e60bfc90b24f045fcb791c4483711ca9c6d09",
         "public_id": "e9572ee6-4b5e-45e4-a840-58a33b04b8a7",
         "username": "my username"}
       ]
    }

1.  Viewing Single User

    ENDPOINT: &ldquo;user/public<sub>id</sub>&rdquo; [GET REQ]
    REQ: admin token
    
    You can get public id of user by sending GET req to &ldquo;user&rdquo; endpoint: see above
    
        requests.get(URL+"/user/public_id", headers=headers)
    
    RESPONSE: 200
    
        {"user":
         {
            "admin": false,
             "id": 2,
             "password": "sha256$f8ulwnAv$8af6f5590e8af54c8d2171cc9afc568727a8a763e8c875855f8b7d27f5dfcccd",
             "public_id": "1f190b06-263s-42aa-86e9-460d0aff93d9",
             "username": "my username"
         }
        }


<a id="orgf794b60"></a>

## Promoting a user

ENDPOINT: &ldquo;user/public<sub>id</sub>&rdquo; [PUT REQ]
REQ: admin token

    headers = {"x-access-token": token}
    requests.put(URL+"/user/public_id", headers=headers)

RESPONSE: 200

    {"message": "The user has been promoted!"}


<a id="orgc4379ee"></a>

## Deleting a user

ENDPOINT: &ldquo;user/public<sub>id</sub>&rdquo; [DELETE REQ]
REQ: admin token

    headers = {"x-access-token": token}
    requests.delete(URL+"/user/public_id", headers=headers)

RESPONSE: 200

    {"message": "The user has been deleted!"}


<a id="org199daa1"></a>

## Creating a post

ENDPOINT: &ldquo;template&rdquo; [POST REQ]

The payload should have title and url and optionally description.

    headers = {"x-access-token": token}
    data = {"title": "some title",
             "url": "http:/test.com",
             "description": "some desc",
             }
    requests.put(URL+"/user/public_id", headers=headers)

RESPONSE: 200

    {"message": "Post created"}


<a id="orgc436b68"></a>

## Viewing post

ENDPOINT: &ldquo;template&rdquo; [GET REQ]

    headers = {"x-access-token": token}
    requests.get(URL+"/template", headers=headers)

RESPONSE: 200

    {"templates": [
        {"description": "Done",
         "id": 27,
         "posted": "Mon, 12 Oct 2020 04:51:27 GMT",
         "title": "Test thing",
         "url": "https://i.imgur.com/yYGxFJX.jpeg",
         "user_id": "alskjdf_dfkdjf"}
       ]
    }

Note: Sometimes user<sub>id</sub>, description can be null.

1.  Viewing Single Post

    ENDPOINT: &ldquo;template/template<sub>id</sub>&rdquo; [GET REQ]
    
    You can get template id of post by sending GET req to &ldquo;template&rdquo; endpoint: see above
    
        requests.get(URL+"/template/template_id", headers=headers)
    
    RESPONSE: 200
    
        {"template":
         {"description": "Done",
             "id": 27,
             "posted": "Mon, 12 Oct 2020 04:51:27 GMT",
             "title": "Test thing",
             "url": "https://i.imgur.com/yYGxFJX.jpeg",
             "user_id": "alskjdf_dfkdjf"
         }
        }
    
    Note: Sometimes user<sub>id</sub>, description can be null too.


<a id="org35efcf3"></a>

## Updating a post

ENDPOINT: &ldquo;template/template<sub>id</sub>&rdquo; [PUT REQ]

Updating a post is same as creating it.

    headers = {"x-access-token": token}
    data = {"title": "some title",
             "url": "http:/test.com",
             "description": "some desc",
             }
    requests.put(URL+"/template/template_id", data=data, headers=headers)

RESPONSE: 200

    {"message": "Post Updated"}


<a id="org392f3b0"></a>

## Deleting a post

ENDPOINT: &ldquo;template/template<sub>id</sub>&rdquo; [DELETE REQ]

    headers = {"x-access-token": token}
    requests.delete(URL+"/template/template_id", headers=headers)

RESPONSE: 200

    {"message": "The post has been deleted"}


<a id="orga9733d7"></a>

# Configuration

All the configs are set in the meme<sub>api</sub>/\_<sub>init</sub>\_<sub>.py</sub> file.


<a id="orgc59a945"></a>

## Installing dependencies

-   With Pip
    
        $ python3 -m venv .venv
        $ .venv/bin/python -m pip install -r requirements.txt
-   With Poetry
    
        $ poetry install


<a id="org9c22f5a"></a>

## Database config

The config SQLALCHEMY<sub>DATABASE</sub><sub>URI</sub> is made from different env vars parts like HOST<sub>NAME</sub>, HOST<sub>PASS</sub> etc You need to set those variables
Or you can just use sqlite db.

A minimal &rsquo;.env&rsquo; config looks like

    export SECRET_KEY='mysecretkey'
    export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    export FLASK_APP=run.py

This same config along with example config for hosted sql (eg MYSQL) server is available in .env<sub>eg</sub> file. Just rename, edit and source this file.

    #+ .env_eg file +#
    export SECRET_KEY='mysecretkey'
    export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    export FLASK_APP=run.py
    
    # For a hosted mysql/postgres server
    # Note: if SQLALCHEMY_DATABASE_URI env var is present these env vars will be ignored & WONT BE USED
    export DB_USERNAME='username of database'
    export DB_PASS='password of database'
    export DB_HOST='host address url of database'
    export DB_NAME='name of db and tablename eg. mysqldb$posts'


<a id="org2dbc4d5"></a>

## Database initialization and migration

Before initializing the database. Create a migrations folder for you db and delete the existing one

    $ rm -rf ./migrations
    $ python -m flask db init # makes migrations folder

Run migrate to create the tables required by the models

    $ python -m flask db migrate
    $ python -m flask db upgrade

Once you make any changes to models you need to migrate & upgrade the database as shown above


<a id="org8cf28e5"></a>

## Setting up migration for existing database

In case you already have a database initialized(ie db schema created) through different option and want to integrate flask-migrate in it.

First: Initialize the migrations folder
Note: delete existing migrations folder

    $ python -m flask db init

Create another empty database table and point the database env variables to this empty table (in case of sqlite just change the &rsquo;site.db&rsquo; name to &rsquo;site2.db&rsquo;)

    $ python -m flask db migrate

Now again point to your original database column in environment vars (for sqlite just change &rsquo;site2.db&rsquo; back to &rsquo;site.db&rsquo;)

    $ python -m flask db stamp head
    $ python -m flask db migrate # you should see 'no change in schema detected' message

You are all set. From now, if you make any changes to models you need to migrate & upgrade the database as shown below

    $ python -m flask db migrate
    $ python -m flask db upgrade


<a id="orgfca0e17"></a>

## Creating an admin user

Only admin users are allowed to create new accounts through api. Thus a admin user has to be manually created (or you could remove that if statement and create user acc through that route)

    import uuid
    
    from werkzeug.security import generate_password_hash
    
    from run import app
    from meme_api import db
    from meme_api.models import User
    
    app.app_context().push()
    
    hashed_pass = generate_password_hash('secretpassword', method='sha256')
    
    admin = User(username='admin',
                 password=hashed_pass,
                 admin=True,
                 public_id=str(uuid.uuid4()) )
    
    db.session.add(admin)
    db.session.commit()


<a id="org80ec986"></a>

# Application registration tokens

The token generated by the api never expires. For preventing leaked tokens to be misued and also limit the database connections, the prod branch of this repo implements a application based registering.

A random uuid is generated and manually put into the meme<sub>api</sub>/apps.py file. This id can now be used in headers for requesting every route.

    #+ apps.py file +
    registered = {
        'application': 'generated random uuid',
        'cli': 'another uuid for another app',
    }

    headers = {
        'x-application-token': 'uuid token for application',
        'x-access-token': 'user login token',
    }

Every routes including login now requires above &rsquo;x-application-token&rsquo; header for the request to be successful.


<a id="orgfc6484c"></a>

# Loosening other routes

With application based authentication in place, the routes for creating new user, getting all posts etc can be loosened to not require an admin token.


<a id="orgece8575"></a>

# TODOS

1.  [ ] Add Tests

2.  [ ] Add Logging

