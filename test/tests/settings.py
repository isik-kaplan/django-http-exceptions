SECRET_KEY = 'TERCES'

INSTALLED_APPS = [
    'tests',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
]

# Templates engines
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Middlewares
MIDDLEWARE = MIDDLEWARE_CLASSES = [
    'django_http_exceptions.middleware.ExceptionHandlerMiddleware',
    'django_http_exceptions.middleware.ThreadLocalRequestMiddleware',
]

ROOT_URLCONF = 'tests.urls'

# Database
DATABASES = {}

# Allow test without database
TEST_RUNNER = 'tests.testing.DatabaselessTestRunner'
