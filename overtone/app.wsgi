activate_this = '/var/data/public/app/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/data/public/app/')

from app import app as application