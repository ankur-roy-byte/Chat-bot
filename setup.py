"""
ChatApp - Real-time messaging application built with Django
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='chatapp',
    version='1.0.0',
    description='A real-time person-to-person messaging application built with Django and WebSockets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ChatApp Team',
    author_email='',
    url='https://github.com/ankur-roy-byte/Chat-bot',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='django chat websocket real-time messaging channels',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django==3.1.14',
        'djangorestframework==3.11.2',
        'django-filter==2.4.0',
        'channels==2.4.0',
        'channels-redis==2.4.2',
        'mysqlclient==1.4.6',
        'Markdown==3.2.1',
        'pytz',
    ],
    extras_require={
        'dev': [
            'pdbpp',
            'coverage',
            'black',
            'flake8',
            'isort',
        ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
        ],
    },
    entry_points={
        'console_scripts': [],
    },
    project_urls={
        'Bug Reports': 'https://github.com/ankur-roy-byte/Chat-bot/issues',
        'Source': 'https://github.com/ankur-roy-byte/Chat-bot',
        'Documentation': 'https://github.com/ankur-roy-byte/Chat-bot/wiki',
    },
)
