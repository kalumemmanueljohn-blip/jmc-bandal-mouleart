from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SÉCURITÉ
# ============================================

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production-123456789')

# DEBUG doit être False en production sur Render
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# ============================================
# APPLICATIONS INSTALLÉES
# ============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    
    # Applications du projet
    'core',
    'accounts',
    'events',
    'teachings',
    'blog',
    'donations',
    'gallery',
    'chat',
    'channels',
]

# ============================================
# MIDDLEWARE
# ============================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# ROOT URLCONF
# ============================================

ROOT_URLCONF = 'jeunesse_eglise.urls'

# ============================================
# TEMPLATES
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ============================================
# AUTHENTIFICATION
# ============================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# ============================================
# DATABASE - SQLite3 (optimisé)
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,
        }
    }
}

# ============================================
# CHANNELS / WEBSOCKET
# ============================================

ASGI_APPLICATION = 'jeunesse_eglise.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ============================================
# INTERNATIONALISATION
# ============================================

USE_TZ = True
TIME_ZONE = 'Africa/Kinshasa'
LANGUAGE_CODE = 'fr-fr'
USE_I18N = True

# ============================================
# FICHIERS STATIQUES ET MÉDIAS
# ============================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ AJOUT POUR LES PDF - Configuration des types MIME
import mimetypes
mimetypes.add_type('application/pdf', '.pdf', True)
mimetypes.add_type('application/octet-stream', '.pdf', False)

# ✅ AJOUT POUR LES FICHIERS EN PRODUCTION
FORCE_SCRIPT_NAME = None

# ============================================
# UPLOAD DE FICHIERS (avec compression)
# ============================================

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# ============================================
# CONFIGURATION DU CHAT
# ============================================

CHAT_TYPING_TIMEOUT = 3
CHAT_MAX_FILES_PER_MESSAGE = 5

CHAT_ALLOWED_FILE_TYPES = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
    'video': ['.mp4', '.mov', '.avi', '.mkv', '.webm'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.webm'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx'],
}

CHAT_MAX_FILE_SIZES = {
    'image': 5 * 1024 * 1024,
    'video': 20 * 1024 * 1024,
    'audio': 10 * 1024 * 1024,
    'document': 10 * 1024 * 1024,
    'default': 10 * 1024 * 1024,
}

CHAT_MESSAGES_PER_PAGE = 50
CHAT_MAX_CONVERSATIONS = 50
CHAT_AUTO_MODERATION_DELAY = 0
CHAT_FILTERED_WORDS = []

# ============================================
# SÉCURITÉ PRODUCTION
# ============================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    # ✅ MODIFICATION POUR LES PDF - Permet de détecter correctement les types de fichiers
    SECURE_CONTENT_TYPE_NOSNIFF = False
