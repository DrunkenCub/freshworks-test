import os

# using https://www.regextester.com/19 
EMAIL_REGEX = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
SECRET_KEY = os.environ.get('FW_SECRET_KEY', 'freshwork-rocks')
DB_CON_STRING = os.environ.get('FW_DB_CON_STRING', 'sqlite:////tmp/test.db')
