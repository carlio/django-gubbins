import urlparse
import urllib

def append_params(url, params):
    url_parts = urlparse.urlparse(url)
    query = urlparse.parse_qsl(url_parts.query)
    for key, value in params.iteritems():
        query.append( (key, value) )
    new_url_parts = list(url_parts)
    new_url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(new_url_parts)
    