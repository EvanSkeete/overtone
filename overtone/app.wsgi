activate_this = '/var/data/public/app/venv/bin/activate'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/data/public/app/overtone/')

from app import app as application