import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-22+dta0)s1#k&l&8u&a_13l=)!((@q7z&t)-(7%$)g@^#(92w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ["mpasha.ddns.net"]
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'accounts.MyUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'login_page',
    'deshbroad',
    'salesUser',
    'product_showcase',
    'paymentSection',
    'pandaApi',
    'administrationSection',
    'rest_framework',
    'rest_framework.authtoken',
    'fcm',
    'import_export',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'panda_automation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'panda_automation.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mendim',
        'USER':'root',
        'PASSWORD':'pritom',
        'HOST':'localhost',
        'PORT':''
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = 'login_view'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

# CELERY_BROKER_URL = 'amqp://pritom:1234@localhost:5672/pritom'
# CELERY_RESULT_BACKEND = 'amqp://pritom:1234@localhost:5672/pritom'
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://localhost'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': (
#        'rest_framework.authentication.TokenAuthentication',
#    ),
#    'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAdminUser'
#    ),
# }

# FCM_APIKEY = "AAAASSL9z7c:APA91bHlpoTvl-h32wzOs-jrfjSQUpU0gW1Qxg-0fXmLSflVXCSWLS7dv9rpFx7VdQVj3oUirGfBspWvTbVhT_nDjZMYUeBLMOhL0mhVnBG-RE-Mzxa9WY3tOCnJ1Tpgg0wvZj3DgEWY"
# FCM_APIKEY = "AAAAdKthgSA:APA91bG7i8kOkklRL5XizdJiQnZtqdCBiXtGK8uU5EUAsQctvsKOlZydcl-W6nP9MuYSa8uXpcXYazRMZHPD9-5BJCyX9xRhdmMrA1aGdI94H0nLMEPKoXhykBOH_D8oSkphpyIgyNA3PbEtlannOECm7bWftnjNHg"
FCM_APIKEY = "AAAAuexHU6U:APA91bGQuHRgUiTIh34vRZ3F6piG31LC7hXiqbvKZ6FZf7y_f5LjGnQs1lEydd3sNs7RfjIffaZl0-1NybFgefGcytHPRjqhgN7Vp3ydLGOKqQlV6aBPVuLCQVC_e_95sImwesRN1R3U"
FCM_MAX_RECIPIENTS=1000
