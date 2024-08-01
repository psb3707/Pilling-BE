import os
from datetime import datetime
workers = 3
bind = 'unix:/run/gunicorn.sock'
accesslog = f"./logs/gunicorn/access_{datetime.now().strftime('%Y_%m_%d')}.log"
errorlog = f"./logs/gunicorn/error_{datetime.now().strftime('%Y_%m_%d')}.log"