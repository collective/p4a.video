from zope.app.annotation import interfaces as annointerfaces
from zope import interface
from p4a.video import interfaces
from p4a.video import metadataextractor

def _safe(v):
    if isinstance(v, list) or isinstance(v, tuple):
        if len(v) >= 1:
            return v[0]
        else:
            return None
    return v

class FLVVideoDataAccessor(object):
    interface.implements(interfaces.IVideoDataAccessor)
    
    def __init__(self, context):
        self._filecontent = context

    @property
    def video_type(self):
        return 'Flash FLV File'

    @property
    def _video(self):
        return interfaces.IVideo(self._filecontent)

    @property
    def _video_data(self):
        annotations = annointerfaces.IAnnotations(self._filecontent)
        return annotations.get(self._video.ANNO_KEY, None)

    def load(self, filename):
        
        metadata = metadataextractor.extract(filename)
        
        self._video_data['height'] = str(metadata.height[0])
        self._video_data['width'] = str(metadata.width[0])
        self._video_data['duration'] = str(metadata.duration[0])

    def store(self, filename):
        pass
        