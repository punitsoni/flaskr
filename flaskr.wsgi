#!/usr/bin/python

import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/local/mnt/workspace/mywork/web/www/flaskr")

from app import app as application
