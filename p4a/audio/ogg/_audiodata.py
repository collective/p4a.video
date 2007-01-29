from zope.app.annotation import interfaces as annointerfaces
from zope import interface
from p4a.audio import interfaces
from p4a.audio.ogg.thirdparty.mutagen.oggvorbis import Open as openaudio

def _safe(v):
    if isinstance(v, list) or isinstance(v, tuple):
        if len(v) >= 1:
            return v[0]
        else:
            return None
    return v

class OggAudioDataAccessor(object):
    interface.implements(interfaces.IAudioDataAccessor)
    
    def __init__(self, context):
        self._filecontent = context

    @property
    def audio_type(self):
        return 'Ogg Vorbis'

    @property
    def _audio(self):
        return interfaces.IAudio(self._filecontent)

    @property
    def _audio_data(self):
        annotations = annointerfaces.IAnnotations(self._filecontent)
        return annotations.get(self._audio.ANNO_KEY, None)

    def load(self, filename):
        oggfile = openaudio(filename)
        
        self._audio_data['title'] = _safe(oggfile['title'])
        self._audio_data['artist'] = _safe(oggfile['artist'])
        self._audio_data['album'] = _safe(oggfile['album'])
        
        self._audio_data['bit_rate'] = long(oggfile.info.bitrate)
        self._audio_data['length'] = long(oggfile.info.length)
        self._audio_data['frequency'] = long(oggfile.info.sample_rate)

    def store(self, filename):
        oggfile = openaudio(filename)
        
        oggfile['title'] = self._audio.title or u''
        oggfile['artist'] = self._audio.artist or u''
        oggfile['album'] = self._audio.album or u''
        
        oggfile.save()
