try:
    # python 3
    from urllib.parse import urlencode, urlparse, urljoin, urlunparse
except ImportError:
    # python 2 backward compatibility
    # noinspection PyUnresolvedReferences
    from urllib import urlencode
    # noinspection PyUnresolvedReferences
    from urlparse import urlparse, urljoin, urlunparse
