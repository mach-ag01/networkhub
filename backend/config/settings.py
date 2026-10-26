import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me") if DEBUG else os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    raise RuntimeError("Set SECRET_KEY when DEBUG=False.")
ALLOWED_HOSTS = [v.strip() for v in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if v.strip()]
INSTALLED_APPS = ["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","corsheaders","rest_framework","django_filters","core"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","corsheaders.middleware.CorsMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES={"default":dj_database_url.parse(os.environ["DATABASE_URL"],conn_max_age=600,ssl_require=not DEBUG)} if os.getenv("DATABASE_URL") else {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="en-us"; TIME_ZONE="Africa/Nairobi"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATIC_ROOT=BASE_DIR/"staticfiles"; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
STORAGES={"default":{"BACKEND":"django.core.files.storage.FileSystemStorage"},"staticfiles":{"BACKEND":"whitenoise.storage.CompressedManifestStaticFilesStorage"}}
CORS_ALLOWED_ORIGINS=[v.strip() for v in os.getenv("CORS_ALLOWED_ORIGINS","http://localhost:5173").split(",") if v.strip()]
CSRF_TRUSTED_ORIGINS=[v.strip() for v in os.getenv("CSRF_TRUSTED_ORIGINS","").split(",") if v.strip()]
SECURE_SSL_REDIRECT=os.getenv("SECURE_SSL_REDIRECT","False" if DEBUG else "True").lower() in ("1","true","yes")
SESSION_COOKIE_SECURE=not DEBUG; CSRF_COOKIE_SECURE=not DEBUG; SECURE_CONTENT_TYPE_NOSNIFF=True; X_FRAME_OPTIONS="DENY"; SECURE_REFERRER_POLICY="strict-origin-when-cross-origin"; SECURE_HSTS_SECONDS=31536000 if not DEBUG else 0
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework_simplejwt.authentication.JWTAuthentication"],"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.AllowAny"],"DEFAULT_FILTER_BACKENDS":["django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"],"DEFAULT_THROTTLE_CLASSES":["rest_framework.throttling.AnonRateThrottle","rest_framework.throttling.UserRateThrottle"],"DEFAULT_THROTTLE_RATES":{"anon":"120/hour","user":"1000/hour","login":"5/minute","register":"5/hour","analytics":"30/minute","contact":"10/hour"},"DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination","PAGE_SIZE":12}
SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME":timedelta(minutes=30),"REFRESH_TOKEN_LIFETIME":timedelta(days=7)}
CACHES={"default":{"BACKEND":"django.core.cache.backends.redis.RedisCache","LOCATION":os.environ["REDIS_URL"]}} if os.getenv("REDIS_URL") else {"default":{"BACKEND":"django.core.cache.backends.locmem.LocMemCache","LOCATION":"networkhub-local"}}
