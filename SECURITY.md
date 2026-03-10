# Security Policy

## Supported Versions

We take security seriously and aim to respond to vulnerabilities promptly. Currently, the following versions are being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow these steps:

### 1. Do Not Disclose Publicly

Please **do not** report security vulnerabilities through public GitHub issues, discussions, or pull requests.

### 2. Submit a Private Report

Instead, please report security vulnerabilities by:

- Opening a private security advisory on GitHub (Preferred method)
- Emailing the maintainers directly with details
- Using GitHub's private vulnerability reporting feature

### 3. Provide Detailed Information

When reporting a vulnerability, please include:

- **Description**: A clear description of the vulnerability
- **Impact**: The potential impact of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Affected Components**: Which parts of the system are affected
- **Suggested Fix**: If you have ideas for how to fix the issue (optional)
- **Environment**: Your environment details (OS, Python version, Django version, etc.)

### 4. Response Timeline

You can expect:

- **Acknowledgment**: Within 48 hours of submission
- **Initial Assessment**: Within 5 business days
- **Status Updates**: Regular updates on the progress
- **Resolution**: We aim to fix critical vulnerabilities within 30 days

### 5. Coordinated Disclosure

We practice coordinated disclosure and will:

1. Work with you to understand and reproduce the issue
2. Develop and test a fix
3. Prepare an advisory
4. Release the fix and publish the advisory
5. Credit you for the discovery (if you wish)

## Security Best Practices

When deploying this application, please follow these security best practices:

### Configuration

- **Change the SECRET_KEY**: Never use the default secret key in production
- **Disable DEBUG**: Set `DEBUG = False` in production
- **Configure ALLOWED_HOSTS**: Properly configure allowed hosts
- **Use HTTPS**: Always use HTTPS in production
- **Secure Cookies**: Enable secure cookie settings

### Database

- **Strong Passwords**: Use strong database passwords
- **Limited Privileges**: Database users should have minimal required privileges
- **Regular Backups**: Implement regular database backups
- **Connection Security**: Use encrypted database connections when possible

### Dependencies

- **Keep Updated**: Regularly update Django and all dependencies
- **Monitor Vulnerabilities**: Use tools like `safety` to check for known vulnerabilities
- **Review Dependencies**: Be cautious about adding new dependencies

### WebSocket Security

- **Authentication**: Ensure WebSocket connections are properly authenticated
- **CORS Configuration**: Properly configure CORS settings
- **Rate Limiting**: Implement rate limiting for WebSocket connections
- **Input Validation**: Validate all WebSocket messages

### Environment Variables

- **Never Commit Secrets**: Never commit secrets to version control
- **Use .env Files**: Use environment variables for sensitive configuration
- **Secure Storage**: Store production secrets in secure secret management systems

### Additional Measures

- **Enable CSRF Protection**: Keep CSRF protection enabled for forms
- **SQL Injection Prevention**: Use Django ORM properly to prevent SQL injection
- **XSS Prevention**: Use Django's template auto-escaping
- **File Upload Security**: If implementing file uploads, validate and sanitize files
- **Logging**: Implement comprehensive security logging
- **Regular Security Audits**: Conduct regular security audits and penetration testing

## Known Security Considerations

### Current Limitations

1. **CSRF on API**: The API currently disables CSRF protection for session authentication. Consider using token-based authentication for production.

2. **Database Credentials**: The default settings include database credentials. These should be moved to environment variables.

3. **Redis Security**: Ensure Redis is not exposed to the internet and is properly secured.

4. **Rate Limiting**: The application does not currently implement rate limiting. Consider adding rate limiting middleware.

## Security Updates

Security updates will be announced through:

- GitHub Security Advisories
- Release notes in CHANGELOG.md
- GitHub Releases

## Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [Django Channels Security](https://channels.readthedocs.io/en/stable/topics/security.html)

## Acknowledgments

We appreciate the security research community and all those who responsibly disclose vulnerabilities to help make this project more secure.
