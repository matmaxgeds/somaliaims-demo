import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BOOTSTRAP3 = {
    # The complete URL to the Bootstrap CSS file
    'css_url': '/static/bootstrap/css/bootstrap.min.css',
    'javascript_url': '/static/bootstrap/js/bootstrap.min.js',
}
