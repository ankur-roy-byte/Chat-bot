# Configuration Guide

This guide covers all configuration options for ChatApp.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Django Settings](#django-settings)
- [Database Configuration](#database-configuration)
- [Redis Configuration](#redis-configuration)
- [Channel Layer Configuration](#channel-layer-configuration)
- [Security Settings](#security-settings)
- [Static Files](#static-files)
- [Email Configuration](#email-configuration)
- [Logging Configuration](#logging-configuration)

## Environment Variables

Copy `.env.example` to `.env` or `chat/local_settings.py` and configure:

```bash
cp .env.example .env
```

### Required Variables

```bash
# Django Secret Key - MUST be changed in production
SECRET_KEY=your-unique-secret-key-here

# Debug mode - MUST be False in production
DEBUG=False

# Allowed hosts - comma-separated list of domains
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database Variables

```bash
DB_ENGINE=django.db.backends.mysql
DB_NAME=chat
DB_USER=chatapp_user
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_PORT=3306
```

### Redis Variables

```bash
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
```

## Django Settings

### Using local_settings.py

Create `chat/local_settings.py` to override settings:

```python
# chat/local_settings.py

# Security
SECRET_KEY = 'your-secret-key-here'
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chatapp_prod',
        'USER': 'chatapp_user',
        'PASSWORD': 'strong-password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Redis/Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}
```

### Using Environment Variables

To use environment variables in Django:

```python
# chat/settings.py
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key-for-development')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('DB_NAME', 'chat'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

## Database Configuration

### MySQL Configuration

#### Basic Setup

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chatapp',
        'USER': 'chatapp_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### Advanced Options

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chatapp',
        'USER': 'chatapp_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

#### Using SSL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chatapp',
        'USER': 'chatapp_user',
        'PASSWORD': 'password',
        'HOST': 'db.example.com',
        'PORT': '3306',
        'OPTIONS': {
            'ssl': {
                'ca': '/path/to/ca-cert.pem',
                'cert': '/path/to/client-cert.pem',
                'key': '/path/to/client-key.pem',
            }
        }
    }
}
```

### PostgreSQL Configuration (Alternative)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chatapp',
        'USER': 'chatapp_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Redis Configuration

### Basic Configuration

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### With Password

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [f'redis://:{password}@127.0.0.1:6379/0'],
        },
    },
}
```

### Redis Sentinel

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                {
                    'sentinels': [
                        ('sentinel1', 26379),
                        ('sentinel2', 26379),
                        ('sentinel3', 26379),
                    ],
                    'master_name': 'mymaster',
                    'db': 0,
                }
            ],
        },
    },
}
```

## Channel Layer Configuration

### Capacity and Expiry

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
            "capacity": 1500,  # Maximum messages per channel
            "expiry": 10,      # Message expiry in seconds
        },
    },
}
```

### Symmetric Encryption

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}
```

## Security Settings

### Production Security Configuration

```python
# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cookie settings
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'
```

### Password Validation

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

## Static Files

### Development

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

### Production

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Optional: Use WhiteNoise for serving static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Email Configuration

### SMTP Configuration

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

### Console Backend (Development)

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Logging Configuration

### Basic Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/chatapp/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

## Application Settings

### Message Configuration

```python
# Number of messages to load per page
MESSAGES_TO_LOAD = 15
```

### REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

## Testing Configuration

### Test Settings

Create `chat/test_settings.py`:

```python
from .settings import *

# Use SQLite for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use in-memory channel layer for tests
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Disable password validation in tests
AUTH_PASSWORD_VALIDATORS = []

# Faster password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
```

Run tests with test settings:
```bash
./manage.py test --settings=chat.test_settings
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check database credentials
   - Verify database server is running
   - Check firewall rules

2. **Redis Connection Errors**
   - Verify Redis is running
   - Check Redis host and port
   - Verify network connectivity

3. **Static Files Not Loading**
   - Run `./manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings
   - Verify web server configuration

## Best Practices

1. **Never commit sensitive data** to version control
2. **Use environment variables** for production secrets
3. **Enable all security settings** in production
4. **Use HTTPS** in production
5. **Regular backups** of database and Redis
6. **Monitor logs** regularly
7. **Keep dependencies updated**

## Additional Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/stable/ref/settings/)
- [Django Channels Configuration](https://channels.readthedocs.io/en/stable/topics/channel_layers.html)
- [Redis Configuration](https://redis.io/documentation)
