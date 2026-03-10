# Contributing to ChatApp

First off, thank you for considering contributing to ChatApp! It's people like you that make this project such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [JavaScript Style Guide](#javascript-style-guide)
- [Testing](#testing)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title** for the issue
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs** if possible
- **Include your environment details** (OS, Python version, Django version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior** and **explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Follow the [Python](#python-style-guide) and [JavaScript](#javascript-style-guide) style guides
- Include thoughtfully-worded, well-structured tests
- Document new code
- End all files with a newline

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/Chat-bot.git
   cd Chat-bot
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   pipenv --python 3 shell
   pipenv install --dev
   ```

3. **Set up the database**
   ```bash
   # Create MySQL database
   mysql -u root -p -e "CREATE DATABASE chat CHARACTER SET utf8;"

   # Run migrations
   ./manage.py migrate
   ```

4. **Start Redis server** (required for WebSocket support)
   ```bash
   redis-server
   ```

5. **Create a superuser**
   ```bash
   ./manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   ./manage.py runserver
   ```

7. **Run tests**
   ```bash
   ./manage.py test
   ```

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐎 `:racehorse:` when improving performance
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - ✅ `:white_check_mark:` when adding tests
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (not tabs)
- Maximum line length is 100 characters
- Use docstrings for all public modules, functions, classes, and methods
- Use meaningful variable names
- Follow Django best practices and conventions

Example:
```python
def calculate_message_stats(user_id):
    """
    Calculate statistics for messages sent by a user.

    Args:
        user_id (int): The ID of the user

    Returns:
        dict: A dictionary containing message statistics
    """
    messages = MessageModel.objects.filter(user_id=user_id)
    return {
        'total': messages.count(),
        'today': messages.filter(timestamp__date=timezone.now().date()).count()
    }
```

### JavaScript Style Guide

- Use 2 spaces for indentation
- Use semicolons
- Use single quotes for strings
- Use meaningful variable and function names
- Comment your code when necessary

## Testing

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage
- Follow existing test patterns in the codebase

```bash
# Run all tests
./manage.py test

# Run specific test file
./manage.py test core.tests.test_model

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.

Thank you for contributing! 🎉
