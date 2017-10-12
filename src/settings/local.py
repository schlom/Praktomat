# Settings for deployment

from os.path import join, dirname, basename
import re

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))
PRAKTOMAT_ID = basename(dirname(PRAKTOMAT_PATH))

match = re.match(r'''
	(?:praktomat_)?
	(?P<oop>OOP_)?
	(?P<swprojekt>SW_Projekt_)?
	(?P<year>\d+)_
	(?P<semester>WS|SS)
	''', PRAKTOMAT_ID, flags=re.VERBOSE)

if match:
	if match.group('oop') is not None:
		SITE_NAME = 'OOP Java Informatik '
	elif match.group('swprojekt') is not None:
		SITE_NAME = 'Softwareprojekt EKT '
	else:
		SITE_NAME = 'Programmieren '

	year = int(match.group('year'))
	if match.group('semester') == "WS":
		SITE_NAME += "Wintersemester %d/%d" % (year, year+1)
	else:
		SITE_NAME += "Sommersemester %d" % year

else:
	raise NotImplementedError("Autoconfig for PRAKTOMAT_ID %s not possible", PRAKTOMAT_ID)

# The name that will be displayed on top of the page and in emails.
#SITE_NAME = 'Praktomat der Frankfurt University of Applied Sciences'

# The URL where this site is reachable. 'http://localhost:8000/'
BASE_HOST = 'http://10.0.2.15:8000' # URL to access
BASE_PATH = '/' + PRAKTOMAT_ID + '/'

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'
STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime. Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "PraktomatSupport/")
#SANDBOX_DIR = join('/home/praktomat/sandbox/', PRAKTOMAT_ID)

# Setting for E-Mail service
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.....com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "praktomat@....de"
EMAIL_HOST_PASSWORD = "..."
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "praktomat@....de"

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':   PRAKTOMAT_ID,
    }
}

#ALLOWED_HOSTS = [ 'praktomat.cs.kit.edu', ]
ALLOWED_HOSTS = ['*']
# Enabled DEBUG is default
#DEBUG = False
DEBUG = True

# SECRET_KEY gets generated via defaults.py
# Private key used to sign uploaded solution files in submission confirmation email
#PRIVATE_KEY = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'privkey.pem')
PRIVATE_KEY = None

# Enable Shibboleth:
SHIB_ENABLED = False

# Set this to False to disable registration via the website, e.g. when Single Sign On is used
REGISTRATION_POSSIBLE = True

ACCOUNT_CHANGE_POSSIBLE = True
DUMMY_MAT_NUMBERS = False
SHOW_CONTACT_LINK = False 

# Use a dedicated user to test submissions
USEPRAKTOMATTESTER = False
TEST_TIMEOUT=600

# It is recomendet to use DOCKER and not a tester account
# for using Docker from https://github.com/nomeata/safe-docker
# Use docker to test submission
USESAFEDOCKER = True

# Various extra files and versions
CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle-6.19-all.jar'
JPLAGJAR = '/srv/praktomat/contrib/jplag-2.11.8-SNAPSHOT-jar-with-dependencies.jar'
JAVA_LIBS = { 'junit3' : '/usr/share/java/junit.jar', 'junit4' : '/usr/share/java/junit4.jar' }

# Our VM has 20 cores, so lets try to use them
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 6

# Finally load defaults for missing settings.
import defaults
defaults.load_defaults(globals())
