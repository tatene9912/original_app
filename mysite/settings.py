from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p8iu-5-=*3=xe+h8l3tcy86xfyga*xtkzr756t$5u$0+b@9#$d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
import os

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'GOODstime.apps.GoodstimeConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_bootstrap5',
    'import_export', 
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'mysite.urls'
SITE_ID = 1


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            ],
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



WSGI_APPLICATION = 'mysite.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', #デフォルトの認証基盤 
    'allauth.account.auth_backends.AuthenticationBackend' # メールアドレスとパスワードの両方を用いて認証するために必要
)

LOGIN_URL = 'account_login' # ログインURLの設定
LOGIN_REDIRECT_URL = 'GOODstime:top' # ログイン後のリダイレクト先
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login' #　ログアウト後のリダイレクト先
# ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.CustomSignupForm'
ACCOUNT_ADAPTER = "accounts.adapter.CustomAccountAdapter"

AUTH_USER_MODEL = "accounts.User" # カスタムユーザーを認証用ユーザーとして登録
# Allauthの設定
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # usernameフィールドを無効化
ACCOUNT_USERNAME_REQUIRED = False  # usernameを不要にする
ACCOUNT_EMAIL_REQUIRED = True  # emailを必須にする
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # emailで認証する
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True  # パスワード確認フィールドを使用する場合
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # メール検証を必須とする

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_local'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s [%(levelname)s] %(message)s"}},
    "handlers": {
        "info": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "handlers": ["info", "warning", "error"],
        "level": "INFO",
    },
}