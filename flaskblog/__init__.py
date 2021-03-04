import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


app = Flask(__name__)
app.config.from_object(Config)
# initialisation of the sqlalchemy database
db = SQLAlchemy(app)
# initialisation of bcrypt
bcrypt = Bcrypt(app)
# initialisation of the loginManager
login_manager = LoginManager(app)
# to limit access to certain pages prior to logging in
login_manager.login_view = 'users.login'
# adding bootstrap styles to the message displayed by the login page
login_manager.login_message_category = 'info'
# initialisation of mail
mail = Mail(app)
# to prevent circular imports we import ur routes after initializing the app in line 5
# we import the blueprint instance -> users from the users/routes
from flaskblog.users.routes import users
# we import the blueprint instance -> posts from the posts/routes
from flaskblog.posts.routes import posts
# we import the blueprint instance -> main from the main/routes
from flaskblog.main.routes import main

# we then register the blueprint imports
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
