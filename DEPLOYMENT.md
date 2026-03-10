# Deployment Guide

This guide provides instructions for deploying ChatApp to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Deployment Options](#deployment-options)
  - [Traditional Server Deployment](#traditional-server-deployment)
  - [Docker Deployment](#docker-deployment)
  - [Cloud Platform Deployment](#cloud-platform-deployment)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Web Server Configuration](#web-server-configuration)
- [ASGI Server Setup](#asgi-server-setup)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying, ensure you have:

- Python 3.6 or higher
- MySQL 5.7 or higher (or compatible database)
- Redis server
- Web server (Nginx or Apache)
- ASGI server (Daphne or Uvicorn)
- SSL certificate (for HTTPS)
- Domain name (recommended)

## Pre-Deployment Checklist

### Security Configuration

- [ ] Change `SECRET_KEY` to a strong, random value
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Set up environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Configure secure cookie settings
- [ ] Review and update CORS settings if applicable
- [ ] Enable CSRF protection
- [ ] Set up proper file permissions

### Database

- [ ] Create production database
- [ ] Configure database user with minimal privileges
- [ ] Set strong database password
- [ ] Enable database backups
- [ ] Run migrations
- [ ] Create initial superuser

### Dependencies

- [ ] Update all dependencies to latest secure versions
- [ ] Run security audit (`pip-audit` or `safety check`)
- [ ] Remove development dependencies from production

### Application

- [ ] Run all tests and ensure they pass
- [ ] Collect static files
- [ ] Configure media file storage
- [ ] Set up logging
- [ ] Configure email settings (if applicable)

## Deployment Options

### Traditional Server Deployment

This is the recommended approach for most deployments.

#### 1. Server Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade

# Install required packages
sudo apt-get install python3 python3-pip python3-venv
sudo apt-get install mysql-server redis-server
sudo apt-get install nginx
```

#### 2. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/chatapp
cd /var/www/chatapp

# Clone repository
git clone https://github.com/ankur-roy-byte/Chat-bot.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn daphne
```

#### 3. Configure Environment

Create `/var/www/chatapp/.env`:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=chatapp_prod
DB_USER=chatapp_user
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_PORT=3306

REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# Add other production settings
```

#### 4. Database Setup

```sql
-- Create database and user
CREATE DATABASE chatapp_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'chatapp_user'@'localhost' IDENTIFIED BY 'strong-password-here';
GRANT SELECT, INSERT, UPDATE, DELETE ON chatapp_prod.* TO 'chatapp_user'@'localhost';
FLUSH PRIVILEGES;
```

```bash
# Run migrations
./manage.py migrate

# Create superuser
./manage.py createsuperuser

# Collect static files
./manage.py collectstatic --noinput
```

### Docker Deployment

For containerized deployment:

#### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn daphne

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chat.asgi:application"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8
    environment:
      MYSQL_DATABASE: chatapp
      MYSQL_USER: chatapp
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: daphne -b 0.0.0.0 -p 8000 chat.asgi:application
    volumes:
      - ./:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    env_file:
      - .env

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

### Cloud Platform Deployment

#### Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: daphne chat.asgi:application --port \$PORT --bind 0.0.0.0" > Procfile
echo "release: python manage.py migrate" >> Procfile

# Deploy
heroku create your-app-name
heroku addons:create heroku-redis:hobby-dev
heroku addons:create cleardb:ignite
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
git push heroku main
```

#### AWS (EC2 + RDS + ElastiCache)

1. Set up RDS MySQL instance
2. Set up ElastiCache Redis instance
3. Launch EC2 instance
4. Follow traditional server deployment steps
5. Configure security groups
6. Set up Application Load Balancer
7. Configure Auto Scaling (optional)

## Web Server Configuration

### Nginx Configuration

Create `/etc/nginx/sites-available/chatapp`:

```nginx
upstream chatapp {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    client_max_body_size 10M;

    location / {
        proxy_pass http://chatapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://chatapp;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/chatapp/staticfiles/;
    }

    location /media/ {
        alias /var/www/chatapp/media/;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/chatapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## ASGI Server Setup

### Daphne with Systemd

Create `/etc/systemd/system/chatapp.service`:

```ini
[Unit]
Description=ChatApp ASGI Server
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/chatapp
Environment="PATH=/var/www/chatapp/venv/bin"
ExecStart=/var/www/chatapp/venv/bin/daphne -b 127.0.0.1 -p 8000 chat.asgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start chatapp
sudo systemctl enable chatapp
sudo systemctl status chatapp
```

### Using Supervisor (Alternative)

Install Supervisor:

```bash
sudo apt-get install supervisor
```

Create `/etc/supervisor/conf.d/chatapp.conf`:

```ini
[program:chatapp]
command=/var/www/chatapp/venv/bin/daphne -b 127.0.0.1 -p 8000 chat.asgi:application
directory=/var/www/chatapp
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/chatapp/daphne.log
```

## SSL/TLS Configuration

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

## Monitoring and Maintenance

### Logging

Configure Django logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/chatapp/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Database Backups

Set up automated backups:

```bash
# Create backup script
cat > /usr/local/bin/backup-chatapp.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/chatapp"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u chatapp_user -p'password' chatapp_prod > $BACKUP_DIR/db_$DATE.sql
gzip $BACKUP_DIR/db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-chatapp.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /usr/local/bin/backup-chatapp.sh" | crontab -
```

### Monitoring Tools

Consider using:

- **Sentry** for error tracking
- **Prometheus + Grafana** for metrics
- **ELK Stack** for log aggregation
- **Uptime monitoring** services

## Troubleshooting

### WebSocket Connection Issues

- Check Nginx WebSocket proxy configuration
- Verify Redis is running and accessible
- Check firewall rules
- Review ASGI server logs

### Database Connection Issues

- Verify database credentials
- Check database server is running
- Verify firewall/security group rules
- Check MySQL user permissions

### Static Files Not Loading

- Run `./manage.py collectstatic`
- Check Nginx static files configuration
- Verify file permissions
- Check STATIC_ROOT setting

### Performance Issues

- Enable database query caching
- Use Redis for session storage
- Implement CDN for static files
- Scale horizontally with load balancer
- Monitor and optimize database queries

## Security Hardening

Additional security measures:

```python
# settings.py production settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## Scaling

For high-traffic scenarios:

1. **Horizontal Scaling**: Deploy multiple application servers behind a load balancer
2. **Database Replication**: Set up read replicas
3. **Redis Cluster**: Use Redis Sentinel or Cluster for high availability
4. **CDN**: Use CloudFlare or similar for static assets
5. **Caching**: Implement application-level caching

## Support

For deployment issues:

- Check the [SECURITY.md](SECURITY.md) for security concerns
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for reporting bugs
- Open an issue on [GitHub](https://github.com/ankur-roy-byte/Chat-bot/issues)

---

**Note**: Always test deployment procedures in a staging environment before applying to production.
