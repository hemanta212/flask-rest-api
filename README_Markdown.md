This is a simple implementation of flask api with JWT(JSON WEB TOKENS). You get a token by logging in and send this token in headers for accessing every other routes.


# Table of Contents

1.  [Implementation Features](#org6553f32)
2.  [Usage](#org704bcc3)
    1.  [Login and get a token](#orge07ff81)
    2.  [Creating a user](#orga2531ad)
    3.  [Viewing user info](#orgf03998e)
    4.  [Promoting a user](#org99d2616)
    5.  [Deleting a user](#org17da2ea)
    6.  [Creating a post](#org3338898)
    7.  [Viewing post](#org9f1bdf8)
    8.  [Updating a post](#orge33aa79)
    9.  [Deleting a post](#org20157c1)
3.  [Configuration](#orgf80e681)
    1.  [Installing dependencies](#org4c89045)
    2.  [Database config](#org66e65a2)
    3.  [Database initialization and migration](#orgd220898)
    4.  [Setting up migration for existing database](#orgabf824d)
    5.  [Creating an admin user](#org8babbe3)
4.  [Application registration tokens](#orgec5c26c)
5.  [Loosening other routes](#orgde17485)
6.  [Useful tools](#org3814e33)
    1.  [Httpie](#org4683aa9)
    2.  [Httpbin.org:](#orgbbd8ff1)
    3.  [Postman (and similar others)](#orgd94974e)
7.  [Inner details](#org91cf6ff)
    1.  [What requests&ldquo; BasicHTTPAuth does](#org79da42f)
    2.  [Diffrent ways to get request data in flask](#org959a991)
8.  [TODOS](#org40dc78b)


<a id="org6553f32"></a>

# Implementation Features

-   Rolling out custom flask decorators
-   Token based auth with jwt
-   Custom application registering and separate client tokens
-   Http Basic username:pass authentication
-   Flask blueprinting for modularization
-   Flask database migration.
-   Supports postgres, sql, sqlite etc dbs with sqlalchemy
-   Returning diffrent http status codes
-   Some common short flask tricks
    -   Defining same routes with diffrent methods to reduce if/else nests
    -   Returning python string, dicts autogenerates a json response (no need jsonify)
    -   Calling .app<sub>context</sub>().push() on flask app instance. Helps a ton in intrepreter to play with db and stuff without initializing


<a id="org704bcc3"></a>

# Usage

This api has user and post tables in db. Every routes relating to &rsquo;user&rsquo; and &rsquo;post&rsquo; requires a token in the header which can be obtained by logging in throgh login route.

This assumes you have completed the configuration, created admin user and have its credentials.[See configuration section](#orgf80e681).

NOTE: Any illegal or failed requests on any route will generate non-200 status code and return a json dict with one &ldquo;message&rdquo; key stating the reason

Example:

    {"message": "no user found"}


<a id="orge07ff81"></a>

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

NOTE: This token has no time limit and will never expire, [see why.](#orgec5c26c) For making expirable tokens have a look at [here](https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp).


<a id="orga2531ad"></a>

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


<a id="orgf03998e"></a>

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


<a id="org99d2616"></a>

## Promoting a user

ENDPOINT: &ldquo;user/public<sub>id</sub>&rdquo; [PUT REQ]
REQ: admin token

    headers = {"x-access-token": token}
    requests.put(URL+"/user/public_id", headers=headers)

RESPONSE: 200

    {"message": "The user has been promoted!"}


<a id="org17da2ea"></a>

## Deleting a user

ENDPOINT: &ldquo;user/public<sub>id</sub>&rdquo; [DELETE REQ]
REQ: admin token

    headers = {"x-access-token": token}
    requests.delete(URL+"/user/public_id", headers=headers)

RESPONSE: 200

    {"message": "The user has been deleted!"}


<a id="org3338898"></a>

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


<a id="org9f1bdf8"></a>

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
         "username": "somerandomusername",
         "posted": true},
    
        {"description": null,
         "id": 27,
         "posted": "Mon, 12 Oct 2020 04:51:27 GMT",
         "title": "Test thing",
         "url": "https://i.imgur.com/yYGxFJX.jpeg",
         "username": null,
         "posted": false},   ]
    }

Note: Sometimes user<sub>id</sub>, description can be null.


### View filtered post

ENDPOINT: &ldquo;/&rdquo; [GET REQ]

The api provides a way to get approved post (with approved propery set to true + current user&rsquo;s own post) with a single api call.

    requests.get(URL+"/", headers=headers)

RESPONSE: 200

    {"templates": [
        {"description": "Done",
         "id": 27,
         "posted": "Mon, 12 Oct 2020 04:51:27 GMT",
         "title": "Test thing",
         "url": "https://i.imgur.com/yYGxFJX.jpeg",
         "username": "somerandomusername",
         "posted": true}
       ]
    }

Note: Sometimes user<sub>id</sub>, description can be null too.


### Viewing Single Post

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


<a id="orge33aa79"></a>

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


<a id="org20157c1"></a>

## Deleting a post

ENDPOINT: &ldquo;template/template<sub>id</sub>&rdquo; [DELETE REQ]

    headers = {"x-access-token": token}
    requests.delete(URL+"/template/template_id", headers=headers)

RESPONSE: 200

    {"message": "The post has been deleted"}


<a id="orgf80e681"></a>

# Configuration

All the configs are set in the meme<sub>api</sub>/\_<sub>init</sub>\_<sub>.py</sub> file.


<a id="org4c89045"></a>

## Installing dependencies

-   With Pip
    
        $ python3 -m venv .venv
        $ .venv/bin/python -m pip install -r requirements.txt
-   With Poetry
    
        $ poetry install


<a id="org66e65a2"></a>

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


<a id="orgd220898"></a>

## Database initialization and migration

Before initializing the database. Create a migrations folder for you db and delete the existing one

    $ rm -rf ./migrations
    $ python -m flask db init # makes migrations folder

Run migrate to create the tables required by the models

    $ python -m flask db migrate
    $ python -m flask db upgrade

Once you make any changes to models you need to migrate & upgrade the database as shown above


<a id="orgabf824d"></a>

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


<a id="org8babbe3"></a>

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


<a id="orgec5c26c"></a>

# Application registration tokens

The token generated by the api never expires. For preventing leaked tokens to be misued and also limit the database connections, the prod branch of this repo implements a application based registering.

A random uuid is generated and manually put into the meme<sub>api</sub>/apps.py file. This id can now be used in headers for requesting every route.

    #+ apps.py file +
    registered = {
        'someapp': 'generated random uuid',
        'cli': 'another uuid for another app',
    }

    headers = {
        'x-application-token': 'uuid token for application',
        'x-access-token': 'user login token',
    }

Every routes including login now requires above &rsquo;x-application-token&rsquo; header for the request to be successful.


<a id="orgde17485"></a>

# Loosening other routes

With application based authentication in place, the routes for creating new user, getting all posts etc can be loosened to not require an admin token.


<a id="org3814e33"></a>

# Useful tools

There are many good tools to leverage understanding of how api&rsquo;s and http requests work.


<a id="org4683aa9"></a>

## [Httpie](https://github.com/httpie/httpie)

-   CLI tools for testing, debugging API endpoints.


<a id="orgbbd8ff1"></a>

## Httpbin.org:

-   An dedicated website which provides post, delete, put etc endpoints in httpbin.org/post, /delete respectivly. Returns all the headers and data info it got in nice json format.
    -   Great partner tool with httpie


<a id="orgd94974e"></a>

## Postman (and similar others)

-   Exploring, testing endpoints with diffrent kinds of requests in a friendly UI. Helps creating a test suite.


<a id="org91cf6ff"></a>

# Inner details


<a id="org79da42f"></a>

## What requests&ldquo; BasicHTTPAuth does

    import requests
    from requests.auth import HTTPBasicAuth
    
    URL = "https://httpbin.org"
    auth = HTTPBasicAuth("username", "password")
    
    login_response = requests.post(URL+"/post", auth=auth)
    
    print(login_response.json())

Response

    {"args": {},
     "data": "",
     "files": {},
     "form": {},
     "headers": {"Accept": "*/*",
                 "Accept-Encoding": "gzip, deflate",
                 "Authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ=",
                 "Content-Length": "0",
                 "Host": "httpbin.org",
                 "User-Agent": "python-requests/2.24.0",
                 "X-Amzn-Trace-Id": "Root=1-5f8aee35-211905107cfea23a2ad3b865"},
     "json": null,
     "origin": "35.229.170.146",
     "url": "https://httpbin.org/post"}

What we are interested in is the Authorization header. Basically the requests transformed the username and password to base64 encoded string and passed the header.

    header = {
        "Authorization": "Basic " + Base64encoded(username + ":" + password)
    }

So instead of passing auth arg we can also create this authorization header ourself and should get the same result


### Implementing own auth header

    import requests
    import base64
    
    URL = "httpbin.org/post"
    token = base64.b64encode(bytes("username:pass", "utf-8"))
    headers  = {"Authorization": f"Basic {token.decode()}"}
    response = requests.get(URL, headers=headers)
    
    print(response.json())

    {"args": {},
     "data": "",
     "files": {},
     "form": {},
     "headers": {"Accept": "*/*",
                 "Accept-Encoding": "gzip, deflate",
                 "Authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ=",
                 "Content-Length": "0",
                 "Host": "httpbin.org",
                 "User-Agent": "python-requests/2.24.0",
                 "X-Amzn-Trace-Id": "Root=1-5f8af1bb-716f15011a1b61770e118a7f"},
     "json": null,
     "origin": "35.229.170.146",
     "url": "https://httpbin.org/post"}


<a id="org959a991"></a>

## Diffrent ways to get request data in flask

Ref: [stackoverflow page](https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request)

-   request.data : used for fallback data storage mostly empty

-   request.args: the key/value pairs in the URL query string

-   request.form:
    the key/value pairs in the body, from a HTML post form, or JavaScript request that isn&rsquo;t JSON encoded

-   request.files:
     the files in the body, which Flask keeps separate from form. HTML forms must
    use enctype=multipart/form-data or files will not be uploaded.

-   request.values:
    combined args and form, preferring args if keys overlap

-   request.json:
    parsed JSON data. The request must have the application/json content type, or
    use request.get<sub>json</sub>(force=True) to ignore the content type.


<a id="org40dc78b"></a>

# TODOS

1.  [ ] Add Tests

2.  [ ] Add Logging

