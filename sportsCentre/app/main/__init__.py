# This file for indicating dirctory of disk into Python package directory 
# <<example - folder structure>>
# mydir/spam/__init__py
# mydir/spam/module.py
# -> import spam.module  (we can access the code of 'module.py') or..
# -> from spam import module (we can access the code of 'module.py')

from flask import Blueprint 

main = Blueprint('main', __name__)

from . import views