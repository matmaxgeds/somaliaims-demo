from .settings import *

# Modify to use postgresql for production on python anywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'somaliaims',
        'USER': 'somaliaims',
        'PASSWORD': 'aims.somali',
        'HOST': 'somaliaims-43.postgres.pythonanywhere-services.com',
        'PORT': '10043',
    }
}

# Enable XSendfile in web server config
SERVE_FILE_BACKEND = 'filetransfers.backends.xsendfile.serve_file'