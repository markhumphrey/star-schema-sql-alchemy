DATABASE_URI = 'sqlite:///db/test.db'

# DATA_FILENAME = '../data/WA_Sales_Products_2012-14.csv'
DATA_FILENAME = '../data/WA_Sales_Products_2012-14-short.csv'


SQLALCHEMY_ENGINE_ECHO = True
# SQLALCHEMY_ENGINE_ECHO = False
# SQLALCHEMY_ENGINE_ECHO = "debug"

try:
    from local_config import *
except ImportError:
    # no local config found
    pass
