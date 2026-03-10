# ChatApp

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-3.1.14-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![Demo](http://g.recordit.co/JYruQDLd0h.gif)

A professional, real-time person-to-person messaging application built with Django, Django Channels, and WebSockets. This application provides instant messaging capabilities with a clean REST API and efficient WebSocket-based notifications.

## ✨ Features

- 🔐 **User Authentication**: Secure login system with Django authentication
- 💬 **Real-time Messaging**: Instant message delivery using WebSockets
- 🔔 **Live Notifications**: Real-time message notifications without polling
- 📱 **REST API**: Clean and well-documented REST API
- 👥 **User Management**: User list and selection interface
- 📊 **Message History**: Browse previous message history
- ⚡ **Scalable Architecture**: Built with Django Channels for horizontal scaling
- 🔄 **Redis Support**: Redis backend for channel layers in production

## 🏗️ Architecture

The application follows a modern WebSocket-based architecture:

1. **User Login**: Frontend downloads user list and establishes WebSocket connection
2. **Message Loading**: When selecting a chat partner, loads the latest 15 messages
3. **Message Sending**: Messages are POSTed to REST API, saved to database, and users are notified via WebSocket
4. **Message Receiving**: Frontend receives notification with message ID and fetches the message via GET request

### Technology Stack

- **Backend**: Django 3.1.14, Django REST Framework
- **Real-time**: Django Channels 2.4.0, channels-redis
- **Database**: MySQL (with index optimization)
- **Cache/Channels**: Redis
- **Authentication**: Django Session Authentication
- **API**: RESTful API with Django REST Framework

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6 or higher
- MySQL 5.7 or higher
- Redis Server
- pip and pipenv
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ankur-roy-byte/Chat-bot.git
cd Chat-bot
```

### 2. Set Up Virtual Environment

```bash
pipenv --python 3 shell
pipenv install
```

Alternatively, using pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Database

Create a MySQL database:
```sql
CREATE DATABASE chat CHARACTER SET utf8;
```

Update database settings in `chat/settings.py` or create `chat/local_settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chat',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Start Redis Server

```bash
redis-server
```

Or on macOS with Homebrew:
```bash
brew services start redis
```

### 5. Run Migrations

```bash
./manage.py migrate
```

### 6. Create Admin User

```bash
./manage.py createsuperuser
```

### 7. Run Tests (Optional)

```bash
./manage.py test
```

### 8. Start Development Server

```bash
./manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## ⚙️ Configuration

### Environment Variables

For production, use environment variables for sensitive data. See `.env.example` for reference.

### Message Prefetch

Configure the number of messages to load per conversation in `chat/settings.py`:
```python
MESSAGES_TO_LOAD = 15
```

### Channel Layers

Development uses Redis as the channel layer backend:
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

For production, consider using Redis Sentinel or Redis Cluster for high availability.

## 📦 Project Structure

```
Chat-bot/
├── chat/               # Django project settings
│   ├── settings.py    # Main settings file
│   ├── urls.py        # URL routing
│   ├── routing.py     # WebSocket routing
│   └── wsgi.py        # WSGI configuration
├── core/              # Main application
│   ├── models.py      # Database models
│   ├── api.py         # REST API views
│   ├── serializers.py # DRF serializers
│   ├── consumers.py   # WebSocket consumers
│   ├── routing.py     # WebSocket URL routing
│   └── tests/         # Test suite
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── manage.py          # Django management script
├── Pipfile           # Pipenv dependencies
└── requirements.txt   # Pip dependencies
```

## 🔄 API Documentation

### Endpoints

#### Messages
- `GET /api/messages/` - List messages
- `GET /api/messages/?target=username` - Get messages with specific user
- `POST /api/messages/` - Send a new message
- `GET /api/messages/{id}/` - Get specific message

#### Users
- `GET /api/users/` - List all users (excluding current user)

### WebSocket

Connect to `/ws/` for real-time notifications.

Message format:
```json
{
    "type": "recieve_group_message",
    "message": "message_id"
}
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
./manage.py test

# Run specific test file
./manage.py test core.tests.test_model

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📈 Scaling

### Horizontal Scaling

Django Channels enables running multiple interface and worker servers:

1. **Interface Servers**: Handle HTTP and WebSocket connections
2. **Worker Servers**: Process background tasks
3. **Channel Layer**: Redis coordinates communication between servers

For more information, see the [Django Channels documentation](https://channels.readthedocs.io/en/latest/introduction.html).

### Database Scaling

- Use database indexes (already implemented on key fields)
- Consider read replicas for high-traffic scenarios
- Implement database connection pooling
- Use MySQL cluster/sharding for very high loads

## 🔒 Security

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS in production
- Implement rate limiting
- Regular security updates

See [SECURITY.md](SECURITY.md) for more details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Known Limitations

This project is a demonstration application and has some limitations:

- No password reset functionality
- No user registration flow
- Limited test coverage
- No frontend framework (vanilla JavaScript)
- No frontend build system
- Basic UI design (Bootstrap-based)
- No user pagination in selector
- No message search functionality
- No file/image sharing
- No group chat support

These are opportunities for future enhancements!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Real-time features powered by [Django Channels](https://channels.readthedocs.io/)
- UI components from [Bootstrap](https://getbootstrap.com/)

## 📞 Support

- 📫 Issues: [GitHub Issues](https://github.com/ankur-roy-byte/Chat-bot/issues)
- 📖 Documentation: See the [docs](https://github.com/ankur-roy-byte/Chat-bot/wiki) (if available)
- 💬 Discussions: [GitHub Discussions](https://github.com/ankur-roy-byte/Chat-bot/discussions)

## 🗺️ Roadmap

Future enhancements being considered:

- [ ] User registration and password reset
- [ ] Modern frontend framework (React/Vue)
- [ ] Enhanced test coverage
- [ ] Message search functionality
- [ ] File and image sharing
- [ ] Group chat support
- [ ] User status indicators
- [ ] Message read receipts
- [ ] Typing indicators
- [ ] Mobile responsive improvements
- [ ] Docker support
- [ ] CI/CD pipeline

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Channels Documentation](https://channels.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Redis Documentation](https://redis.io/documentation)

---

**Note**: This is a demonstration/learning project. For production use, additional security hardening, testing, and features should be implemented.

Made with ❤️ by the ChatApp team
