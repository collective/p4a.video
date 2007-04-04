from zope import interface
from zope.app.annotation import interfaces as annointerfaces
from p4a.video import interfaces
from p4a.video import metadataextractor

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

MISSING = [None]

class AbstractDataAccessor(object):
    interface.implements(interfaces.IVideoDataAccessor)

    def __init__(self, context):
        self._filecontent = context

    @property
    def _video(self):
        video = getattr(self, '__cached_video', None)
        if video is not None:
            return video
        self.__cached_video = interfaces.IVideo(self._filecontent)
        return self.__cached_video

    @property
    def _video_data(self):
        annotations = annointerfaces.IAnnotations(self._filecontent)
        return annotations.get(self._video.ANNO_KEY, None)

    def _setup_data(self, metadata, attr, type_):
        self._video_data[attr] = getattr(metadata, attr, MISSING)[0]
        if self._video_data[attr] != None:
            self._video_data[attr] = type_(self._video_data[attr])

    def load(self, filename):
        metadata = metadataextractor.extract(filename)

        self._setup_data(metadata, 'height', int)
        self._setup_data(metadata, 'width', int)
        self._setup_data(metadata, 'duration', float)

    def store(self, filename):
        raise NotImplementedError('Write support not yet implemented')
