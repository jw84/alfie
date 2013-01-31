import urllib
import base64
import json

_httplib = None
try:
    from google.appengine.api import urlfetch
    _httplib = 'urlfetch'
except ImportError:
    pass

if not _httplib:
    import urllib2
    _httplib = "urllib2"

api_key = "8xc2JMjUQp9PwQMDsjXBy62sp-uzUC4g"
base_url = 'https://www.geteasypost.com/api'

headers = {
    'User-Agent': 'EasyPost-Python-v1',
    'Authorization': 'Basic %s' % (base64.b64encode(api_key + ':'), )
}

class EasyPost(object):

    def __init__(self, key=None):
        self.api_key = key

    @classmethod
    def api_url(cls, ttype='', action=''):
        return '%s/%s/%s' % (base_url, ttype, action)

    @classmethod
    def post(cls, url, params):
        data = cls.encode(params)
        if _httplib == "urlfetch":
            res = urlfetch.fetch(url, payload=data, headers=headers, method="POST")
            return json.loads(res.content)
        else:
            req = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(req)
            response_html = response.read()
            return json.loads(response_html)

    # The following methods in the EasyPost class are taken from Stripe's python bindings
    # which are under the MIT licnese. See https://github.com/stripe/stripe-python
    @classmethod
    def encode_dict(cls, stk, key, dictvalue):
        n = {}
        for k, v in dictvalue.iteritems():
            k = cls._utf8(k)
            v = cls._utf8(v)
            n["%s[%s]" % (key, k)] = v
        stk.extend(cls._encode_inner(n))

    @classmethod
    def _encode_inner(cls, d):
        """
        We want post vars of form:
        {'foo': 'bar', 'nested': {'a': 'b', 'c': 'd'}}
        to become:
        foo=bar&nested[a]=b&nested[c]=d
        """
        # special case value encoding
        ENCODERS = {
            dict: cls.encode_dict
        }

        stk = []
        for key, value in d.iteritems():
            key = cls._utf8(key)
            try:
                encoder = ENCODERS[value.__class__]
                encoder(stk, key, value)
            except KeyError:
                # don't need special encoding
                value = cls._utf8(value)
                stk.append((key, value))
        return stk

    @classmethod
    def _utf8(cls, value):
        if isinstance(value, unicode):
            return value.encode('utf-8')
        else:
            return value

    @classmethod
    def encode(cls, d):
        """
        Internal: encode a string for url representation
        """
        return urllib.urlencode(cls._encode_inner(d))

# End of Stripe methods.


class Address(object):
    def __init__(self):
        pass

    @classmethod
    def verify(cls, **address):
        params = {
            'address': address
        }
        return EasyPost.post(EasyPost.api_url("address", "verify"), params)


class Postage(object):
    def __init__(self):
        pass

    @classmethod
    def rates(cls, **data):
        return EasyPost.post(EasyPost.api_url("postage", "rates"), data)

    @classmethod
    def compare(cls, **data):
        return Postage.rates(**data)

    @classmethod
    def buy(cls, **data):
        return EasyPost.post(EasyPost.api_url("postage", "buy"), data)

    @classmethod
    def get(cls, filename):
        return EasyPost.post(EasyPost.api_url("postage", "get"), {"label_file_name": filename})

    @classmethod
    def list(cls):
        return EasyPost.post(EasyPost.api_url("postage", "list"), {})