import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'fake-key-for-testing'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'mcpx',  # Our package
]

# Add the MCP_AUTH setting needed by our tests
MCP_AUTH = "test-token"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ROOT_URLCONF = 'tests.urls'

# Use a fast hasher for testing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
