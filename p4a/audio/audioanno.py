from persistent.dict import PersistentDict
from zope import component
from zope import event
from zope import interface
from zope.app.annotation import interfaces as annointerfaces
from zope.app.event import objectevent
from p4a.audio import interfaces
from p4a.fileimage import DictProperty

class AudioAnnotationAddedEvent(objectevent.ObjectEvent):
    """Annotations added to an object for audio metadata.
    """

class AnnotationAudio(object):
    """An IAudio adapter designed to handle ATCT based file content.
    """
    
    interface.implements(interfaces.IAudio)

    ANNO_KEY = 'p4a.audio.audioanno.AnnotationAudio'

    def __init__(self, context):
        self.context = context
        annotations = annointerfaces.IAnnotations(context)
        self.audio_data = annotations.get(self.ANNO_KEY, None)
        if self.audio_data is None:
            self.audio_data = PersistentDict()
            annotations[self.ANNO_KEY] = self.audio_data
            event.notify(AudioAnnotationAddedEvent(self))


    title = DictProperty(interfaces.IAudio['title'], 'audio_data')
    artist = DictProperty(interfaces.IAudio['artist'], 'audio_data')
    album = DictProperty(interfaces.IAudio['album'], 'audio_data')
    year = DictProperty(interfaces.IAudio['year'], 'audio_data')
    genre = DictProperty(interfaces.IAudio['genre'], 'audio_data')
    comment = DictProperty(interfaces.IAudio['comment'], 'audio_data')

    variable_bit_rate = DictProperty(interfaces.IAudio['variable_bit_rate'], 
                                     'audio_data')
    bit_rate = DictProperty(interfaces.IAudio['bit_rate'], 'audio_data')
    frequency = DictProperty(interfaces.IAudio['frequency'], 'audio_data')
    length = DictProperty(interfaces.IAudio['length'], 'audio_data')
    file = DictProperty(interfaces.IAudio['file'], 'audio_data')
    audio_image = DictProperty(interfaces.IAudio['audio_image'], 'audio_data')

    audio_type = DictProperty(interfaces.IAudio['audio_type'], 'audio_data')
