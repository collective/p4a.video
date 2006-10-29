from persistent.dict import PersistentDict
from zope import component
from zope import event
from zope import interface
from zope.app.annotation import interfaces as annointerfaces
from zope.app.event import objectevent
from p4a.video import interfaces
from p4a.fileimage import DictProperty

class VideoAnnotationAddedEvent(objectevent.ObjectEvent):
    """Annotations added to an object for video metadata.
    """

class AnnotationVideo(object):
    """An IVideo adapter designed to handle ATCT based file content.
    """
    
    interface.implements(interfaces.IVideo)

    ANNO_KEY = 'p4a.video.videoanno.AnnotationVideo'

    def __init__(self, context):
        self.context = context
        annotations = annointerfaces.IAnnotations(context)
        self.video_data = annotations.get(self.ANNO_KEY, None)
        if self.video_data is None:
            self.video_data = PersistentDict()
            annotations[self.ANNO_KEY] = self.video_data
            event.notify(VideoAnnotationAddedEvent(self))


    title = DictProperty(interfaces.IVideo['title'], 'video_data')
    artist = DictProperty(interfaces.IVideo['artist'], 'video_data')
    year = DictProperty(interfaces.IVideo['year'], 'video_data')
    comment = DictProperty(interfaces.IVideo['comment'], 'video_data')

    bit_rate = DictProperty(interfaces.IVideo['bit_rate'], 'video_data')
    frequency = DictProperty(interfaces.IVideo['frequency'], 'video_data')
    length = DictProperty(interfaces.IVideo['length'], 'video_data')
    file = DictProperty(interfaces.IVideo['file'], 'video_data')
    video_image = DictProperty(interfaces.IVideo['video_image'], 'video_data')

    video_type = DictProperty(interfaces.IVideo['video_type'], 'video_data')
