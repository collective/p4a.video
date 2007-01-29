DEFAULT_CHARSET = 'utf-8'

def unicodestr(v, charset=DEFAULT_CHARSET):
    """Return the unicode object representing the value passed in an
    as error-immune manner as possible.
    
      >>> unicodestr(u'foo')
      u'foo'
      >>> unicodestr('bar')
      u'bar'
      >>> unicodestr('héllo wórld', 'ascii')
      u'h\\ufffd\\ufffdllo w\\ufffd\\ufffdrld'
    """

    if isinstance(v, unicode):
        return v
    if isinstance(v, str):
        return v.decode(charset, 'replace')
    return unicode(v)
