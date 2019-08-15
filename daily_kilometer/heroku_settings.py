from .settings import *
import django_heroku

DOMAIN = 'http://dailykm.herokuapp.com'

django_heroku.settings(locals())
