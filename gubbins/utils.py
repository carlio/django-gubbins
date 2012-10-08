import urlparse
import urllib
import random 

def random_models(qs, count):
    objects = []
    total_count = qs.count()
    ids = set()
    if total_count > 0:
        while len(objects) < min(count, total_count):
            idx = random.randint(0, total_count - 1)
            obj = qs[idx]
            if obj.id in ids:
                continue
            objects.append(obj)
            ids.add(obj.id)

    return objects


def append_params(url, params):
    url_parts = urlparse.urlparse(url)
    query = urlparse.parse_qsl(url_parts.query)
    for key, value in params.iteritems():
        query.append( (key, value) )
    new_url_parts = list(url_parts)
    new_url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(new_url_parts)

