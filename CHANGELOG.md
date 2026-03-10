# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive CONTRIBUTING.md with contribution guidelines
- CODE_OF_CONDUCT.md for community standards
- SECURITY.md with security policy and vulnerability reporting
- requirements.txt for pip-based installations
- Enhanced README.md with badges, better formatting, and detailed documentation
- .env.example for environment configuration template
- Comprehensive .gitignore for Python/Django projects
- CHANGELOG.md to track version history
- .editorconfig for consistent coding styles across IDEs
- DEPLOYMENT.md with deployment instructions

### Changed
- Improved project documentation for professional standards
- Enhanced README with detailed setup instructions and API documentation

### Security
- Documented security best practices in SECURITY.md
- Added guidance for secure configuration in production

## [1.0.0] - 2019-04-06

### Added
- Real-time messaging using Django Channels 2
- WebSocket support for instant notifications
- REST API for message operations
- User authentication and session management
- Message history with pagination
- Redis backend for channel layers
- MySQL database support with optimized indexes
- Bootstrap-based UI
- Basic test coverage

### Changed
- Migrated to pipenv for package management
- Updated to Django Channels 2 from Channels 1
- Switched to Redis as the channel layer backing store

### Technical Details
- Django 3.1.14 framework
- Django REST Framework for API
- Django Channels 2.4.0 for WebSockets
- channels-redis 2.4.2 for Redis integration
- MySQL database with utf8 charset
- Session-based authentication

## [0.1.0] - Initial Development

### Added
- Basic chat functionality
- Person-to-person messaging
- User management
- Simple WebSocket implementation
- In-memory channel layer
- Basic REST API

---

## Release Notes

### Version Numbering

This project follows Semantic Versioning:
- MAJOR version for incompatible API changes
- MINOR version for added functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes

### How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to propose changes and contribute to this changelog.

### Links

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Project Repository](https://github.com/ankur-roy-byte/Chat-bot)
