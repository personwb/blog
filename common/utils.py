
from django.contrib.sites.models import Site

from mysite.settings import MAIN_DOMAIN

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger("default")


def parse_to_url(obj):

    return _parse_to_url(obj, "https")


def parse_to_url_https(obj):

    return _parse_to_url(obj, "https")


def parse_to_url_http(obj):

    return _parse_to_url(obj, "http")


def _parse_to_url(obj, pre):

    root_url = '%s://%s' % (pre, MAIN_DOMAIN)

    result = str(root_url) + str(obj)

    return result
