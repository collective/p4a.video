from zope.app.annotation import interfaces as annointerfaces
from zope import interface
from p4a.video import interfaces
from p4a.video.ogg.thirdparty.mutagen.oggvorbis import Open as openvideo

def _safe(v):
    if isinstance(v, list) or isinstance(v, tuple):
        if len(v) >= 1:
            return v[0]
        else:
            return None
    return v

class OggVideoDataAccessor(object):
    interface.implements(interfaces.IVideoDataAccessor)
    
    def __init__(self, context):
        self._filecontent = context

    @property
    def video_type(self):
        return 'Ogg Vorbis'

    @property
    def _video(self):
        return interfaces.IVideo(self._filecontent)

    @property
    def _video_data(self):
        annotations = annointerfaces.IAnnotations(self._filecontent)
        return annotations.get(self._video.ANNO_KEY, None)

    def load(self, filename):
        oggfile = openvideo(filename)
        
        self._video_data['title'] = _safe(oggfile['title'])
        self._video_data['artist'] = _safe(oggfile['artist'])
        self._video_data['album'] = _safe(oggfile['album'])
        
        self._video_data['bit_rate'] = long(oggfile.info.bitrate)
        self._video_data['length'] = long(oggfile.info.length)
        self._video_data['frequency'] = long(oggfile.info.sample_rate)

    def store(self, filename):
        oggfile = openvideo(filename)
        
        oggfile['title'] = self._video.title or u''
        oggfile['artist'] = self._video.artist or u''
        oggfile['album'] = self._video.album or u''
        
        oggfile.save()
