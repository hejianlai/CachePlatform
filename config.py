class Config:
    SECRET_KEY = 'the quick brown fox jumps over the lazy dog'
    EXPIRATION = 3600
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:7758258@218.205.104.27:12306/python?charset=utf8'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
