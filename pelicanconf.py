#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime
import urlparse

AUTHOR = u'Alex Moiseenko'
SITENAME = u'IMDagger'
SITEURL = ''

PATH = 'content/'

TIMEZONE = 'Europe/Minsk'
LOCALE = 'ru_RU.UTF-8'
DEFAULT_LANG = u'ru'

ALT_MONTHES = {
    1: u'января',
    2: u'февраля',
    3: u'марта',
    4: u'апреля',
    5: u'мая',
    6: u'июня',
    7: u'июля',
    8: u'августа',
    9: u'сентября',
    10: u'октября',
    11: u'ноября',
    12: u'декабря',
}

BIRTHDAY = datetime(1988, 2, 8)
NOW = datetime.now()

ME = {
    'AGE': NOW.year - BIRTHDAY.year - int(bool(NOW.replace(year=BIRTHDAY.year) < BIRTHDAY)),
    'SEXTYPE': 'male',
    'LOCATION': (u'Гомель', u'Беларусь'),
    'PHOTO': {
        'url': '#',
        'article': None,
    }
}

POST_TYPE_NAMES = {
    'text': u'текст',
    'description': u'обращение',
    'mood': u'настроение',
    'video': u'видео',
    'photo': u'фото',
    'link': u'ссылки',
    'join': u'клубы',
    'friend': u'дружба',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_MAX_ITEMS = 0

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
class Link(object):

    def __init__(self, content, href):
        self.content = content
        self.special_address = href

    def __unicode__(self):
        return unicode(self.content)

SOCIAL = (('email', Link('imdagger@yandex.ru', 'mailto:imdagger@yandex.ru')),
          ('ya online', 'imdagger@ya.ru'),
          ('icq', '350395088'),)

DEFAULT_PAGINATION = 10

THEME = './yaru/'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins',]
PLUGINS = [
    'plugins.edited',
    'plugins.bootstrap_rst_directives',
    'pelican_youtube',
    'pelican_vimeo',
    'extended_sitemap',
]

USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'text'

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'

def getdomain(value):
    if not value:
        return ''
    else:
        return urlparse.urlsplit(value).netloc

JINJA_FILTERS = {
    'domain': getdomain,
}

PYGMENTS_RST_OPTIONS = {
    'classprefix': 'pgcss-',
}

TAG_CLOUD_MAX_ITEMS = 20

STATIC_PATHS = [
    'extra/favicon.ico',
]
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {
        'path': 'favicon.ico',
    },
}

CONTENT_CACHING_LAYER = 'generator'

EXTENDED_SITEMAP_PLUGIN = {
    'priorities': {
        'index': 1.0,
        'articles': 0.9,
        'pages': 0.5,
        'others': 0.0,
    },
    'changefrequencies': {
        'index': 'daily',
        'articles': 'weekly',
        'pages': 'monthly',
        'others': 'never',
    }
}

#PAGINATION_PATTERNS = (
#    (1, '{base_name}/', '{base_name}/index.html'),
#    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
#)
from pelican import paginator
paginator.Page.end_index = 'hello'