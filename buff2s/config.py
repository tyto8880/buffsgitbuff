import os

class Config(object):
    # config class allows to set configuration for future
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'buffs_git_buff'
