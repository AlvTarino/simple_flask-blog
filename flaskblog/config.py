import os


class Config:
    # secret key to prevent XS attacks and SQL injections
    SECRET_KEY = "e83ba48914c7f748783ac7af1f836358fd9788e6cafdd7497d20541c23c7996d"
    # setting up sqlite URI
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    # Mail constants / configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
