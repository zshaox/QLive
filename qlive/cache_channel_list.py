from werkzeug.contrib.cache import SimpleCache
import Qcloud_live


cache = SimpleCache()

def CacheChannel():
    req = cache.get('channel_list')
    if req is None:
        q = Qcloud_live.QQlive()
        req = q.channel_list()
        cache.set('channel_list', req, timeout=600)
    return req
