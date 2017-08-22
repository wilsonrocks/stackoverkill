import os
os.path.join(os.path.dirname(__file__))

import sys
sys.path.insert(0, '/srv/webapps/stackoverkill')
sys.path.insert(0, '/usr/local/lib/python3.6/site-packages')


from stackoverkill import app as application
